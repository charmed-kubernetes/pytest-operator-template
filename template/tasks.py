from pathlib import Path

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
