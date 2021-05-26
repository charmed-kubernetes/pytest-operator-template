import shutil
import subprocess
from pathlib import Path

import yaml

import pytest


def pytest_addoption(parser):
    parser.addoption("--provider", action="store", default="machine")


@pytest.fixture(scope="session")
def provider(pytestconfig):
    return pytestconfig.getoption("provider")


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
    subprocess.check_call(
        ["charmcraft", "init", "--author", "Pytest Conftest"], cwd=tmp_dir
    )
    shutil.copytree(tmp_dir, charm_dir)
    shutil.rmtree(tmp_dir)
    return charm_dir


@pytest.fixture()
def answers(provider):
    """Default answers data for copier"""
    answers = {}
    answers["class_name"] = "TemplateTestCharm"
    # Note "TestCharm" can't be used, that's the name of the deafult unit test class
    answers["charm_type"] = provider
    return answers


@pytest.fixture(scope="session", autouse=True)
def modify_metadata(charm_dir, provider):
    """Modify the metadata based on the charm type"""
    if provider == "machine":
        metadata_file = charm_dir / "metadata.yaml"
        metadata = yaml.safe_load(metadata_file.read_text())
        metadata["series"] = ["focal"]
        del metadata["containers"]
        del metadata["resources"]
        metadata_file.write_text(yaml.dump(metadata))


@pytest.fixture(scope="session")
def github_actions(charm_dir):
    """Load the github actions"""
    actions_file = charm_dir / ".github" / "workflows" / "tests.yaml"
    actions = yaml.safe_load(actions_file.read_text())
    return actions
