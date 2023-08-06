import subprocess

import pytest

from quixote.inspection.exec import background_bash, command, CompletedProcess
from quixote.inspection import InternalError, KOError, TimeoutError


class TestCompletedProcess:
    def test_return_code(self):
        p = CompletedProcess(subprocess.run("true"))
        assert p.return_code == 0

    def test_output(self):
        p = CompletedProcess(subprocess.run("true", capture_output=True))
        assert p.raw_stdout == b""
        assert p.raw_stderr == b""
        assert p.stdout == ""
        assert p.stderr == ""

    def test_output_without_capturing(self):
        p = CompletedProcess(subprocess.run("true"))
        assert p.raw_stdout is None
        assert p.raw_stderr is None
        assert p.stdout is None
        assert p.stderr is None

    def test_check(self):
        CompletedProcess(subprocess.run("true")).check("error")

        with pytest.raises(KOError):
            CompletedProcess(subprocess.run("false")).check("error")

    def test_check_with_custom_exception(self):
        with pytest.raises(InternalError):
            CompletedProcess(subprocess.run("false")).check("error", error_kind=InternalError)

    def test_check_with_custom_statuses(self):
        CompletedProcess(subprocess.run("false")).check("error", allowed_status=1)

        with pytest.raises(KOError):
            CompletedProcess(subprocess.run("true")).check("error", allowed_status=1)

    def test_check_decode(self):
        CompletedProcess(
            subprocess.run("/bin/echo 'hello'", capture_output=True, shell=True)
        ).check("error")

        with pytest.raises(KOError):
            CompletedProcess(
                subprocess.run("/bin/echo -ne '\\xf0\\x90\\x28\\xbc'", capture_output=True, shell=True)
            ).check_decode("error")

    def test_check_decode_with_custom_exception(self):
        with pytest.raises(InternalError):
            CompletedProcess(
                subprocess.run("/bin/echo -ne '\\xf0\\x90\\x28\\xbc'", capture_output=True, shell=True)
            ).check_decode("error", error_kind=InternalError)


class TestCommand:
    def test_env(self):
        p = command("printenv A", env={"A": "1"})
        assert p.stdout == "1\n"

    def test_timeout(self):
        with pytest.raises(TimeoutError):
            command("sleep 1", timeout=0)


class TestBackgroundBash:
    def test_manual_kill(self):
        with background_bash("sleep 10") as p:
            assert p.is_running()
            p.kill()
            assert not p.is_running()

    def test_kill_on_scope_exit(self):
        with background_bash("sleep 10") as p:
            assert p.is_running()
        assert not p.is_running()
