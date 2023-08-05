import re
import shlex
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import click

from sym.cli.helpers.ansible import create_ssh_bin
from sym.cli.helpers.config import SymConfigFile
from sym.cli.helpers.os import has_command
from sym.cli.helpers.params import get_ssh_user
from sym.cli.helpers.ssh import ssh_key_and_config

BINARIES = [
    "aws-cli",
    "ssh",
    "session-manager-plugin",
    "sym",
    "python",
    "aws-okta",
    "saml2aws",
]

REMOTE_LOG_DIRS = ["/var/log/amazon/ssm"]

TEST_PLAYBOOK = """
---
- name: Ping
  hosts: all
  become: true

  tasks:
    - ping:
"""

INSTANCE_PATTERN = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+:\sok=")


def self_update() -> Optional[str]:
    if not has_command("pipx"):
        return None
    version = get_version("sym")
    try:
        subprocess.run(["pipx", "upgrade", "sym-cli"], capture_output=True)
    except subprocess.CalledProcessError:
        return None
    if version != (new_version := get_version("sym")):
        return new_version


def check_saml_client(client, path: Path):
    message = f"client: {client.__class__.__name__}\nis_setup:{client.is_setup()}"
    click.secho(message, fg="blue")
    path.write_text(message)


def get_version(binary) -> Optional[str]:
    if not has_command(binary):
        return None
    for command in ("--version", "-V", "version"):
        result = subprocess.run([binary, command], capture_output=True, text=True)
        if not result.returncode and (output := (result.stdout or result.stderr).strip()):
            return output


def get_versions():
    versions = {}
    for binary in BINARIES:
        versions[binary] = get_version(binary)
        click.secho(f"Found {binary} with version {versions[binary]}", fg="blue")
    return versions


def write_versions(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(f"{k}\t\t{v}" for k, v in get_versions().items()))


def logs_dir(temp_dir: Path) -> Path:
    return temp_dir / f"Sym Logs ({datetime.now().date()} {round(time.time())})"


def zip_logs(doctor_dir: Path) -> Path:
    zip = SymConfigFile(file_name=f"doctor/logs/{doctor_dir.name}")
    shutil.make_archive(str(zip.path), format="zip", root_dir=str(doctor_dir.parent))
    return zip.path.with_suffix(".zip")


def run_and_log_args(args, **kwargs):
    click.secho(f"Running {shlex.join(args)}", fg="blue")
    return subprocess.run(args, capture_output=True, text=True, **kwargs)


def get_server_logs(client, doctor_dir: Path, instance: str):
    click.secho(f"Getting server logs from {instance}", fg="blue", bold=True)

    dest_dir = doctor_dir / "server_logs"
    dest_dir.mkdir(parents=True, exist_ok=True)

    ssh_user = get_ssh_user()
    ssh_bin = str(create_ssh_bin(client))
    ssh_key, _ = ssh_key_and_config(client)

    for dir in REMOTE_LOG_DIRS:
        ssh_commands = [
            f"mkdir -p /tmp/sym{dir}",
            f"sudo cp -r {dir}/ /tmp/sym{dir}",
            f"sudo chmod -R a+rw /tmp/sym{dir}",
        ]
        run_and_log_args(
            ["sym", "ssh", client.resource, instance, "; ".join(ssh_commands)]
        )

        run_and_log_args(
            [
                "scp",
                "-r",
                "-i",
                str(ssh_key),
                "-S",
                str(ssh_bin),
                f"{ssh_user}@{instance}:/tmp/sym{dir}",
                str(dest_dir),
            ]
        )

        ssh_commands = [
            f"cd /tmp/sym",
            f"rm -r /tmp/sym{dir}",
        ]
        run_and_log_args(
            ["sym", "ssh", client.resource, instance, "; ".join(ssh_commands)]
        )


def run_ansible_doctor(
    client, doctor_dir: Path, inventory: Optional[str], playbook: Optional[str],
):
    if not playbook:
        playbook_path = doctor_dir.parent / "playbook.yml"
        playbook_path.write_text(TEST_PLAYBOOK)
        playbook = str(playbook_path)

    args = ["sym", "ansible-playbook", client.resource]
    if inventory:
        args.extend(["-i", inventory])
    args.append(playbook)

    result = run_and_log_args(args)
    if (match := INSTANCE_PATTERN.search(result.stdout)) :
        get_server_logs(client, doctor_dir, match[1])
