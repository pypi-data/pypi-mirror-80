from contextlib import ExitStack
from textwrap import dedent
from typing import Optional, Tuple

from ..decorators import intercept_errors, run_subprocess
from ..helpers.config import SymConfigFile
from ..helpers.contexts import push_envs
from ..helpers.params import get_ssh_user
from ..helpers.ssh import ssh_key_and_config
from ..helpers.tee import Tee
from ..saml_clients.aws_profile import AwsCredentialsPath, AwsProfile

AnsibleSSHPath = "ansible/ssh"
AnsibleSSHProfile = "sym-ansible"


def create_ssh_bin(client):
    proxy_client = client.clone(klass=AwsProfile, resource=AnsibleSSHProfile)
    ssh_bin = proxy_client.subconfig(AnsibleSSHPath)

    command = f'sym {proxy_client.cli_options} ssh {proxy_client.resource} "$@"'
    if (log_dir := client.options.log_dir) :
        command = Tee.tee_command(log_dir, command)

    # fmt: off
    ssh_bin.put(dedent(
        f"""
        #!/bin/bash

        export PYTHONUNBUFFERED=1

        {command}
        """
    ).lstrip())
    # fmt: on
    ssh_bin.path.chmod(0o755)
    return ssh_bin


def run_ansible(
    client: "SAMLClient",
    command: Tuple[str, ...],
    ansible_aws_profile: Optional[str],
    ansible_sym_resource: Optional[str],
    binary: str = "ansible",
):
    client.dprint(f"creating SSH artifacts")

    ssh_bin = str(create_ssh_bin(client))
    ssh_key, _ = ssh_key_and_config(client)
    args = [
        binary,
        *command,
        f"--user={get_ssh_user()}",
        f"--private-key={ssh_key}",
        f"--scp-extra-args=-S '{ssh_bin}'",
        f"--sftp-extra-args=-S '{ssh_bin}'",
    ]
    envs = {
        "ANSIBLE_SSH_EXECUTABLE": ssh_bin,
        "ANSIBLE_SSH_RETRIES": str(2),
        "ANSIBLE_SSH_ARGS": "-C -o ControlMaster=auto -o ControlPersist=15m",
    }

    if client.debug:
        args.append("-vvvv")
        envs["ANSIBLE_SSH_ARGS"] = "-o Compression=no -o ControlMaster=no"
        envs["ANSIBLE_DEBUG"] = str(1)

    client.write_creds(path=AwsCredentialsPath, profile=AnsibleSSHProfile)

    if ansible_aws_profile:
        ansible_client = client.clone(klass=AwsProfile, resource=ansible_aws_profile)
    elif ansible_sym_resource:
        ansible_client = client.clone(resource=ansible_sym_resource)
    else:
        ansible_client = client

    client.dprint(f"running ansible: client='{ansible_client._cli_options}', envs={envs}")

    with push_envs(envs):
        ansible_client.exec(*args, suppress_=True)
