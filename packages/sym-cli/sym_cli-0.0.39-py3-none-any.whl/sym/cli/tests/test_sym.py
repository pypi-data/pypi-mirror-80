from contextlib import contextmanager

import pytest
from click import BadParameter

from sym.cli.helpers.config import Config
from sym.cli.helpers.contexts import push_env
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.sandbox import Sandbox


def test_login(click_setup):
    with click_setup(set_org=False) as runner:
        result = runner.invoke(
            click_command, ["login", "--org", "sym", "--email", "y@symops.io"]
        )
        assert result.exit_code == 0
        assert result.output == "Sym successfully initalized!\n"


def test_ssh_no_login(click_setup):
    with click_setup(set_org=False) as runner:
        result = runner.invoke(click_command, ["ssh", "test", "127.0.0.1"])
        assert result.exit_code > 0
        assert result.output == "Error: Please run `sym login` first\n"


def test_resources(click_setup):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["resources"])
        assert result.exit_code == 0
        assert result.output == "test (Test)\n"


def test_exec(click_setup, saml_client):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["exec", "test", "--", "aws"])
        assert result.exit_code == 0


def test_env_vars(click_setup):
    with click_setup() as runner:
        with push_env("SYM_RESOURCE", "test"):
            result = runner.invoke(click_command, ["version", "--help"])
            assert result.exit_code == 0
            assert "--resource=test" in result.output


def test_env_vars_invalid(click_setup):
    with click_setup() as runner:
        with push_env("SYM_RESOURCE", "tesst"):
            result = runner.invoke(click_command, ["version"])
            assert result.exit_code == BadParameter.exit_code
            assert "--resource=tesst" in result.output
