import logging
import yaml
from pathlib import Path

import pytest

log = logging.getLogger(__name__)


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test):
    my_charm = await ops_test.build_charm(".")
    await ops_test.model.deploy(my_charm)
    await ops_test.model.wait_for_idle()


async def test_status(ops_test):
    metadata = Path("./metadata.yaml")
    charm_name = yaml.safe_load(metadata.read_text())["name"]
    assert (
        ops_test.model.applications[charm_name].units[0].workload_status
        == "Active and running"
    )
