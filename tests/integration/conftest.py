import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def session_folder(tmp_path_factory):
    return tmp_path_factory.mktemp("session")


@pytest.fixture(scope="session")
def src_template(session_folder):
    """Copes the repository into a folder for testing.
    Any uncommited code will be comitted
    A tag of 'Test' will be added to the last commit
    """
    cwd = Path(".")
    destination = session_folder / "src_template"
    shutil.copytree(cwd, destination)
    subprocess.check_call(
        ["git", "config", "user.email", "pytest@example.com"], cwd=destination
    )
    subprocess.check_call(["git", "config", "user.name", "Pytest"], cwd=destination)
    subprocess.check_call(["git", "add", "-A"], cwd=destination)
    try:
        subprocess.check_output(
            ["git", "commit", "-am", "Test check in"], cwd=destination
        )
    except subprocess.CalledProcessError as e:
        if "nothing to commit" not in e.output.decode("utf8"):
            raise
    subprocess.check_call(["git", "tag", "Test"], cwd=destination)

    return destination


@pytest.fixture(scope="session")
def charm_dir(session_folder):
    charm_dir = session_folder / "charm-dir"
    tmp_dir = Path("charm-dir")
    tmp_dir.mkdir()
    subprocess.check_call(["charmcraft", "init"], cwd=tmp_dir)
    shutil.copytree(tmp_dir, charm_dir)
    shutil.rmtree(tmp_dir)
    return charm_dir

@pytest.fixture()
def answers():
    """Default answers data for copier"""
    answers = {}
    answers["charm_name"] = "test-charm"
    return answers
