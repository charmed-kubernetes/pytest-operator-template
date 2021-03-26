import subprocess

import copier


class TestTemplate:
    def test_pytest(self, src_template):
        """Check the fixtures"""
        assert src_template.exists()

    def test_clone(self, src_template, charm_dir, answers):
        """Verify the template clones into a charm"""
        # Remove default charm template for now and use the built in one
        included_charm = charm_dir / "src" / "charm.py"
        included_charm.unlink()
        copier.copy(str(src_template), str(charm_dir), data=answers)
        subprocess.check_call(["git", "add", "."], cwd=charm_dir)
        subprocess.check_call(
            ["git", "commit", "-m", "Template applied"], cwd=charm_dir
        )
        test_data = charm_dir / "tests" / "data"
        test_unit = charm_dir / "tests" / "unit"
        test_integration = charm_dir / "tests" / "integration"
        assert test_data.exists()
        assert test_unit.exists()
        assert test_integration.exists()

    # Removed until the default template is used
    # def test_unit_test_migrated(self, charm_dir):
    #     """Verify default test_charm.py is moved"""
    #     test_charm = charm_dir / "tests" / "test_charm.py"
    #     test_charm_expected = charm_dir / "tests/unit/test_charm.py"
    #     assert not test_charm.exists()
    #     assert test_charm_expected.exists()

    # def test_tasks_removed(self, charm_dir):
    #     """Verify copiers tasks.py is removed"""
    #     tasks = charm_dir / "tasks.py"
    #     assert not tasks.exists()

    def test_update(self, src_template, charm_dir):
        """Verify update restores changes"""
        tox_file = charm_dir / "tox.ini"
        tox_original = tox_file.read_text()
        tox_file.write_text("FILE MODIFIED")
        tox_modified = tox_file.read_text()
        subprocess.check_call(["git", "commit", "-am", "Tox modified"], cwd=charm_dir)
        subprocess.check_call(["copier", "update"], cwd=charm_dir)
        tox_update = tox_file.read_text()
        assert tox_original != tox_modified
        assert tox_original == tox_update

    # def test_integration_test_contents(self, charm_dir, answers):
    #     """Verify the template is processed correctly"""
    #     test_file = charm_dir / "tests" / "integration" / "test_charm.py"
    #     assert test_file.exists()
    #     contents = test_file.read_text()
    #     assert "class IntegrationTest" in contents

    def test_github_actions_created(self, github_actions):
        """Verify github_actions are created as expected"""
        jobs = github_actions["jobs"]
        assert "lint" in jobs
        assert "unit-test" in jobs
        assert "integration-test" in jobs

    def test_github_actions_provider(self, github_actions, provider):
        """Verify the setup is for machines"""
        integration_test = github_actions["jobs"]["integration-test"]
        setup = None
        for step in integration_test["steps"]:
            if step["name"] == "Setup operator environment":
                setup = step
                break
        if provider == "container":
            assert setup["with"]["provider"] == "microk8s"

        else:
            assert setup["with"]["provider"] == "lxd"

    def test_run_lint(self, charm_dir):
        """Try running the templated integration test"""
        subprocess.check_call(["tox", "-e", "lint"], cwd=charm_dir)

    def test_run_unit(self, charm_dir):
        """Try running the templated integration test"""
        subprocess.check_call(["tox", "-e", "unit"], cwd=charm_dir)

    def test_run_integration(self, charm_dir, metadata):
        """Try running the templated integration test"""
        subprocess.check_call(["tox", "-e", "integration"], cwd=charm_dir)
