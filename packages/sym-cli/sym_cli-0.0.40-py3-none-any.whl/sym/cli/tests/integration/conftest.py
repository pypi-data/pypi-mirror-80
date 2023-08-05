from contextlib import contextmanager

import pytest
from click.testing import CliRunner
from expects import *

from sym.cli.sym import sym as click_command
from sym.cli.tests.matchers import succeed


@pytest.fixture
def integration_runner(capfdbinary, sandbox):
    @contextmanager
    def context():
        runner = CliRunner()
        with sandbox.push_xdg_config_home():

            def run(*args):
                result = runner.invoke(click_command, args, catch_exceptions=False)
                cap = capfdbinary.readouterr()
                result.stdout_bytes = cap.out
                result.stderr_bytes = cap.err

                expect(result).to(succeed())
                return result

            yield run

    return context


def pytest_addoption(parser):
    parser.addoption("--email", default="ci@symops.io")
    parser.addoption("--org", default="sym")
    parser.addoption("--instance", default="i-01073e9d0438334fc")
    parser.addoption("--resource", default="test")
