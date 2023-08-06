import re
import shlex
import subprocess
from contextlib import contextmanager
from typing import Any, Iterator, List, Pattern, Sequence, Tuple, Union

from _pytest.monkeypatch import MonkeyPatch
from expects import *


class CaptureCommand:
    def __init__(self, monkeypatch: MonkeyPatch):
        self.monkeypatch = monkeypatch
        self.commands: List[List[str]] = []
        self.outputs = []
        self.matched_outputs: List[Tuple[Pattern, str, int]] = []
        self.allowed_calls = []
        self._run = getattr(subprocess, "run")

    def _get_output(self, args: Sequence[str]):
        command = shlex.join(args)
        for (pattern, output, exit_code) in self.matched_outputs:
            if pattern.search(command):
                if exit_code:
                    raise subprocess.CalledProcessError(exit_code, args, stderr=output)
                return output
        if self.outputs:
            return self.outputs.pop(0)

    # This function is designed for capturing the run_subprocess decorator only.
    # It is not intended to capture subprocess.run calls generally. For example,
    # `args` has a much more constrained type than subprocess.run normally allows.
    def _run_stub(
        self, args: Sequence[str], **kwargs: Any
    ) -> subprocess.CompletedProcess:
        self.commands.append(list(args))
        if args[0] in self.allowed_calls:
            return self._run(args, **kwargs)
        output = self._get_output(args)
        return subprocess.CompletedProcess(args=args, returncode=0, stdout=output)

    @contextmanager
    def __call__(self) -> Iterator[None]:
        with self.monkeypatch.context() as mp:
            mp.setattr(subprocess, "run", self._run_stub)
            yield

    def enqueue_outputs(self, *outputs: Sequence[str]) -> None:
        self.outputs.extend(outputs)

    def register_output(self, pattern: str, output: str, exit_code=0) -> None:
        self.matched_outputs.append((re.compile(pattern), output, exit_code))

    def allow_call(self, binary: str) -> None:
        self.allowed_calls.append(binary)

    def assert_command(self, *commands: Union[str, Sequence[str]]) -> None:
        expect(self.commands).to(have_len(len(commands)))
        for (actual, expected) in zip(self.commands, commands):
            if isinstance(expected, Pattern):
                expect(shlex.join(actual)).to(match(expected))
            elif isinstance(expected, list):
                expect(actual).to(contain(*expected))
            else:
                expect(actual).to(equal(shlex.split(expected)))
