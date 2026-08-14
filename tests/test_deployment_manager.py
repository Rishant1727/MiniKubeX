from deployment.manager import (
    DeploymentManager
)

from deployment.models.deployment import (
    DeploymentSpec
)


def test_create_deployment():

    manager = DeploymentManager()

    spec = DeploymentSpec(
        name="payment-api",
        image="nginx",
        replicas=3
    )

    result = manager.create_deployment(
        spec
    )

    assert result.name == "payment-api"
    assert result.image == "nginx"
    assert result.replicas == 3
    assert result.version == 1
    assert result.status == "pending"