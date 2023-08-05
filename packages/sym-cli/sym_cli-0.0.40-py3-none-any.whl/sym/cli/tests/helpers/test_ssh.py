from multiprocessing import Pool
from uuid import UUID

import click
import pytest

from sym.cli.helpers.config import SymConfigFile
from sym.cli.helpers.ssh import maybe_gen_ssh_key, ssh_key_and_config
from sym.cli.sym import sym as click_command
from sym.cli.tests.conftest import empty_saml_client, setup_context
from sym.cli.tests.helpers.sandbox import Sandbox


def _gen_ssh_key_fn(_i=0):
    with setup_context():
        maybe_gen_ssh_key(empty_saml_client())


def test_gen_ssh_key(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        with Pool(processes=4) as pool:
            pool.map(_gen_ssh_key_fn, range(10))

        ssh_key, _ = ssh_key_and_config(empty_saml_client())
        with ssh_key as f:
            assert "BEGIN OPENSSH PRIVATE KEY" in f.read()


def test_gen_ssh_key_exists(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        _gen_ssh_key_fn()
        ssh_key, _ = ssh_key_and_config(empty_saml_client())

        with ssh_key as f:
            key = f.read()

        with Pool(processes=4) as pool:
            pool.map(_gen_ssh_key_fn, range(10))

        with ssh_key as f:
            assert key == f.read()
