from deployment.models.deployment import (
    DeploymentStatus
)

from deployment.state import (
    DeploymentState
)


def test_deployment_state_create():

    state = DeploymentState()

    deployment = DeploymentStatus(
        name="payment-api",
        image="nginx",
        replicas=3
    )

    state.create(deployment)

    result = state.get(
        "payment-api"
    )

    assert result is not None
    assert result.name == "payment-api"
    assert result.replicas == 3


def test_deployment_state_update():

    state = DeploymentState()

    deployment = DeploymentStatus(
        name="payment-api",
        image="nginx",
        replicas=3
    )

    state.create(deployment)

    deployment.image = "nginx:latest"
    deployment.version = 2

    state.update(deployment)

    result = state.get(
        "payment-api"
    )

    assert result.version == 2
    assert result.image == "nginx:latest"


def test_deployment_rollback():

    state = DeploymentState()

    deployment = DeploymentStatus(
        name="payment-api",
        image="nginx:v1",
        replicas=3,
        version=1
    )

    state.create(deployment)

    deployment.image = "nginx:v2"
    deployment.version = 2

    state.update(deployment)

    result = state.rollback(
        "payment-api"
    )

    assert result is not None
    assert result.image == "nginx:v1"
    assert result.version == 1