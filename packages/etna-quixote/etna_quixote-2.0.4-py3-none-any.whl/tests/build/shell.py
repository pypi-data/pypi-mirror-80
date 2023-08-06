from contextlib import contextmanager

from quixote import new_context
from quixote.build.output import get_output, new_output
from quixote.build import shell, GeneratorType


class TestDockerGenerator:
    @contextmanager
    def setup(self):
        with new_context(generator=GeneratorType.DOCKER):
            with new_output():
                yield

    def test_command(self):
        with self.setup():
            shell.command("ls -lR")
            assert get_output()[-1] == "RUN ls -lR"
            shell.command("apt-get install mysql-common", env={"DEBIAN_FRONTEND": "noninteractive"})
            assert get_output()[-1] == "RUN DEBIAN_FRONTEND=noninteractive apt-get install mysql-common"

    def test_set_env(self):
        with self.setup():
            shell.set_env(ONE="1", TWO="2", WELCOMEMSG="Hello, World!")
            assert get_output()[-1] == "ENV ONE=1 TWO=2 WELCOMEMSG='Hello, World!'"
