import docker

from deployment.container_manager import (
    ContainerManager
)


def test_container_manager_creates_container():

    manager = ContainerManager()

    result = manager.create_container(
        deployment_name="test-api",
        image="nginx",
        version=1,
        replica=1
    )

    client = docker.from_env()

    try:

        container = client.containers.get(
            result["id"]
        )

        assert (
            container.name
            == "minikubex-test-api-v1-1"
        )

        assert container.status == "running"

    finally:

        container.remove(
            force=True
        )