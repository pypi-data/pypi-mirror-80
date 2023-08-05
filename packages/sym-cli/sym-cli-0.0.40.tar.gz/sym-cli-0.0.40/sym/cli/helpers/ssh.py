import os
import re
import sys
import tempfile
from datetime import timedelta
from pathlib import Path
from signal import SIGPIPE, signal
from subprocess import CalledProcessError
from textwrap import dedent
from typing import Sequence

from ..decorators import intercept_errors, retry, run_subprocess
from ..errors import (
    AccessDenied,
    FailedSubprocessError,
    MissingPublicKey,
    SuppressedError,
    TargetNotConnected,
    WrappedSubprocessError,
)
from ..helpers.boto import send_ssh_key, ssm_session
from ..helpers.config import Config, SymConfigFile
from ..helpers.params import get_ssh_user
from ..helpers.sym_group import SymGroup
from ..saml_clients.saml_client import SAMLClient

MissingPublicKeyPattern = re.compile(r"Permission denied \(.*publickey.*\)")
TargetNotConnectedPattern = re.compile("TargetNotConnected")
AccessDeniedPattern = re.compile("AccessDeniedException")
ConnectionClosedPattern = re.compile(r"Connection to .* closed")

SSHConfigPath = "ssh/config"
SSHKeyPath = "ssh/key"


def ssh_key_and_config(client: SAMLClient):
    ssh_key = SymConfigFile(file_name=SSHKeyPath, uid_scope=False)
    ssh_config = client.subconfig(SSHConfigPath, ssh_key=str(ssh_key))
    return (ssh_key, ssh_config)


@intercept_errors()
@run_subprocess
def _gen_ssh_key(dest: SymConfigFile):
    with dest.exclusive_create() as f:
        Path(f.name).unlink(missing_ok=True)
        yield "ssh-keygen", {"t": "rsa", "f": f.name, "N": ""}


def gen_ssh_key(dest: SymConfigFile):
    try:
        _gen_ssh_key(dest, capture_output_=True, input_="n\n")
    except FailedSubprocessError:
        if not dest.path.exists():
            raise


def maybe_gen_ssh_key(client):
    ssh_key, _ = ssh_key_and_config(client)
    if not ssh_key.path.exists():
        gen_ssh_key(ssh_key)


def ssh_args(client, instance, port) -> tuple:
    _, ssh_config = ssh_key_and_config(client)
    opts = {
        "p": str(port),
        "F": str(ssh_config),
        "l": get_ssh_user(),
        "v": client.debug,
    }
    return (
        "ssh",
        instance,
        opts,
        f"-o HostKeyAlias={instance}",
    )


@run_subprocess
def _start_background_ssh_session(client: SAMLClient, instance: str, port: int, *command):
    yield (
        *ssh_args(client, instance, port),
        {"f": True},
        "-o BatchMode=yes",
        *command,
    )


@run_subprocess
def _start_ssh_session(client: SAMLClient, instance: str, port: int, *command: str):
    yield (*ssh_args(client, instance, port), *command)


@intercept_errors(suppress=True)
@run_subprocess
def raw_ssh(*args):
    yield ("ssh", *args)


@retry(TargetNotConnected, delay=1, count=2)
@retry(MissingPublicKey, delay=0, count=2)
def start_ssh_session(
    client: SAMLClient,
    instance: str,
    port: int,
    *,
    args: Sequence[str] = [],
    command: Sequence[str] = [],
    wrap: bool = True,
):
    ensure_ssh_key(client, instance, port)
    client.dprint("starting SSH session")
    try:
        _start_ssh_session(client, instance, port, *args, *command)
    except CalledProcessError as err:
        if ConnectionClosedPattern.search(err.stderr):
            raise SuppressedError(err, echo=True) from err
        client.dprint(f"SSH Session Error: {err.stderr}")
        Config.touch_instance(instance, error=True)
        if MissingPublicKeyPattern.search(err.stderr):
            raise MissingPublicKey(err, get_ssh_user()) from err
        # If the ssh key path is cached then this doesn't get intercepted in ensure_ssh_key
        elif TargetNotConnectedPattern.search(err.stderr):
            raise TargetNotConnected() from err
        elif AccessDeniedPattern.search(err.stderr):
            raise AccessDenied() from err
        else:
            if wrap:
                raise WrappedSubprocessError(
                    err, f"Contact your Sym administrator.", report=True
                ) from err
            else:
                raise SuppressedError(err, echo=True)
    else:
        Config.touch_instance(instance)


@retry(TargetNotConnected, delay=1, count=2)
@intercept_errors({TargetNotConnectedPattern: TargetNotConnected}, suppress=True)
def ensure_ssh_key(
    client,
    instance: str,
    port: int,
    *,
    ttl: timedelta = timedelta(days=1),
    args: Sequence[str] = [],
):
    ssh_key, ssh_config = ssh_key_and_config(client)
    sym_cmd = f"PYTHONUNBUFFERED=1 sym {client.cli_options} ssh-session {client.resource} --instance %h --port %p"
    ssh_cp = Path(tempfile.gettempdir()) / "sym" / "cp"

    if client.debug:
        mux_config = f"""
            ControlMaster no
        """
    else:
        mux_config = f"""
            ControlMaster auto
            ControlPersist 15m
            ControlPath {str(ssh_cp / "%r@%h:%p")}
        """

    # fmt: off
    ssh_config.put(dedent(  # Ensure the SSH Config first, always
        f"""
        Host *
            IdentityFile {str(ssh_key)}
            IdentitiesOnly yes
            PreferredAuthentications publickey
            PubkeyAuthentication yes
            StrictHostKeyChecking no
            PasswordAuthentication no
            ChallengeResponseAuthentication no
            GSSAPIAuthentication no
            ProxyCommand sh -c "{sym_cmd} || exit $?"
            {mux_config.strip()}
        """
    ))
    # fmt: on

    client.dprint("writing SSH key")

    ssh_cp.mkdir(parents=True, exist_ok=True)
    maybe_gen_ssh_key(client)

    if Config.check_instance_ttl(instance, ttl):
        client.dprint(f"Skipping remote SSH key check for {instance}")
        return

    try:
        _start_background_ssh_session(
            client, instance, port, *args, "exit", capture_output_=True
        )
    except CalledProcessError as err:
        client.dprint(f"SSH Check Error: {err.stdout}")
        if not MissingPublicKeyPattern.search(err.stderr):
            raise
        send_ssh_key(client, instance, ssh_key)
    else:
        client.dprint("remote SSH key check succeeded")
        Config.touch_instance(instance)


def start_tunnel(client, instance: str, port: int):
    SymGroup.reset_tees()
    client.dprint("execing aws ssm")

    def handler(signum, frame):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        # Set error state on session end.
        # If the connection was actually successful,
        # the parent thread will re-set a success state.
        # This is the only reliable way to avoid error
        # loops with Ansible due to missing SSH public keys.
        Config.touch_instance(instance, error=True)

    signal(SIGPIPE, handler)

    with ssm_session(client, instance, port) as command:
        client.exec(*command, suppress_=True)
