from controller.models.deployment import Deployment
from controller.reconciler import Reconciler


def test_controller_creates_missing_replicas():

    deployment = Deployment(
        name="payment-api",
        image="nginx",
        replicas=3
    )

    reconciler = Reconciler()

    result = reconciler.reconcile(
        deployment,
        actual_replicas=2
    )

    assert result["action"] == "create"
    assert result["count"] == 1


def test_controller_removes_extra_replicas():

    deployment = Deployment(
        name="payment-api",
        image="nginx",
        replicas=3
    )

    reconciler = Reconciler()

    result = reconciler.reconcile(
        deployment,
        actual_replicas=4
    )

    assert result["action"] == "remove"
    assert result["count"] == 1


def test_controller_does_nothing_when_state_matches():

    deployment = Deployment(
        name="payment-api",
        image="nginx",
        replicas=3
    )

    reconciler = Reconciler()

    result = reconciler.reconcile(
        deployment,
        actual_replicas=3
    )

    assert result["action"] == "none"
    assert result["count"] == 0