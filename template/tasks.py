import fileinput
import os
import subprocess
from pathlib import Path

import yaml
from invoke import task


@task
def migrate_test_charm(c):
    """Migrates the templated test charm if it exists"""
    test_charm = Path("./tests/test_charm.py")
    if test_charm.exists():
        destination = Path("./tests/unit/test_charm.py")
        print(f"Moving {test_charm} to {destination}")
        if destination.exists():
            print(f"Not moving {test_charm}, existing file found: {destination}")
            return
        test_charm.replace(destination)


@task
def remove_tasks(c):
    """Removes the invoke tasks"""
    task = Path("tasks.py")
    if task.exists():
        task.unlink()


@task
def black(c):
    """Runs black formatter"""
    subprocess.check_call(["black", "-v", "."])


@task
def check_yaml(c):
    """If the yaml files are empty, uncomment the default examples"""
    for file_to_process in (Path("./config.yaml"), Path("./actions.yaml")):
        if not file_to_process.exists():
            continue
        if yaml.safe_load(file_to_process.read_text()):
            continue
        with fileinput.input(file_to_process, inplace=1) as f:
            for line in f:
                if ":" in line:
                    line = line[1:]  # Remove the comment prefix
                print(line, end="")


@task
def charm_permissions(c):
    """Make sure charm.py is executable"""
    charm = Path("src/charm.py")
    if charm.exists():
        os.chmod(charm, 0o755)


@task
def remove_unused_files(c):
    """Remove files that aren't used form the standard template"""
    files = []
    run_tests = Path("run_tests")
    files.append(run_tests)
    requirements_dev = Path("requirements-dev.txt")
    files.append(requirements_dev)
    # This can be used and moved instead of deleted when using the upstream template
    test_charm = Path("tests/test_charm.py")
    files.append(test_charm)
    for file in files:
        if file.exists():
            file.unlink()
