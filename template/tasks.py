import fileinput
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
    task.unlink()


@task
def black(c):
    """Runs black formatter"""
    subprocess.check_call(["black", "-v", "."])


@task
def check_yaml(c):
    """If the yaml files are empty, uncomment the default examples"""
    config_file = Path("config.yaml")
    config = yaml.safe_load(config_file.read_text())
    action_file = Path("actions.yaml")
    actions = yaml.safe_load(action_file.read_text())
    if not config and not actions:
        with fileinput.input((action_file, config_file), inplace=1) as f:
            for line in f:
                if ":" in line:
                    line = line[1:]  # Remove the comment prefix
                print(line, end="")
