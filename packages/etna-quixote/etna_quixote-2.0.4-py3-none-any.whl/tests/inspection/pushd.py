import os
import tempfile

from quixote.inspection.pushd import pushd


def test_pushd_simple():
    with tempfile.TemporaryDirectory() as d1:
        current_directory = os.getcwd()
        with pushd(d1):
            assert os.getcwd() == d1
        assert os.getcwd() == current_directory


def test_pushd_nested():
    with tempfile.TemporaryDirectory() as d1:
        with tempfile.TemporaryDirectory() as d2:
            current_directory = os.getcwd()
            with pushd(d1):
                assert os.getcwd() == d1
                with pushd(d2):
                    assert os.getcwd() == d2
                assert os.getcwd() == d1
            assert os.getcwd() == current_directory
