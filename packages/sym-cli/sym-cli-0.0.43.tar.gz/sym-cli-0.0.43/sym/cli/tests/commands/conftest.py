from contextlib import contextmanager
from typing import Sequence

import pytest
from expects import *

from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox
from sym.cli.tests.matchers import fail_with, succeed


@pytest.fixture
def command_tester(
    click_context,
    click_setup,
    ssm_bins,
    env_creds,
    boto_stub,
    saml_client: SAMLClient,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def tester(command: Sequence[str], setup=None, teardown=None):
        stubs = []

        def make_stub(service):
            stub = boto_stub(service)
            stubs.append(stub)
            return stub

        if setup:
            setup()

        @contextmanager
        def context(setup=None, exception=None):
            with click_setup() as runner:
                with click_context:
                    if setup:
                        setup(make_stub)

                with capture_command():
                    result = runner.invoke(click_command, command)
                    if exception:
                        expect(result).to(fail_with(exception))
                    else:
                        expect(result).to(succeed())
                    yield result

                for stub in stubs:
                    stub.assert_no_pending_responses()

                if teardown:
                    teardown()

        return context

    return tester
