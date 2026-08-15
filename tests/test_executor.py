import pytest

from deployment.executor import DeploymentExecutor
from controller.state import ClusterState


class FakeRuntime:

    def __init__(self):

        self.removed = []

    def ensure_image(
        self,
        image: str
    ):

        if image == "invalid:image":
            raise RuntimeError(
                "Image not found"
            )

    def list_containers(self):

        return []

    def create_container(
        self,
        image: str,
        name: str
    ):

        raise RuntimeError(
            "Should not create container"
        )

    def stop_container(
        self,
        container_id: str
    ):

        self.removed.append(
            container_id
        )

    def remove_container(
        self,
        container_id: str
    ):

        self.removed.append(
            container_id
        )


def test_invalid_image_does_not_modify_containers():

    runtime = FakeRuntime()

    cluster_state = ClusterState()

    executor = DeploymentExecutor(
        runtime=runtime,
        cluster_state=cluster_state
    )

    with pytest.raises(
        RuntimeError,
        match="Image not found"
    ):

        executor.execute(
            deployment_name="payment-api",
            image="invalid:image",
            replicas=3
        )

    assert runtime.removed == []