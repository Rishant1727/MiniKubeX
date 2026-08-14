from health.monitor import HealthMonitor
from health.models.status import HealthStatus


class FakeContainer:

    def __init__(
        self,
        container_id,
        name,
        status
    ):

        self.id = container_id
        self.name = name
        self.status = status


def test_running_container_is_healthy():

    container = FakeContainer(
        "container-1",
        "payment-api-1",
        "running"
    )

    monitor = HealthMonitor()

    result = monitor.check_container(
        container
    )

    assert result.status == HealthStatus.HEALTHY


def test_stopped_container_is_unhealthy():

    container = FakeContainer(
        "container-2",
        "payment-api-2",
        "exited"
    )

    monitor = HealthMonitor()

    result = monitor.check_container(
        container
    )

    assert result.status == HealthStatus.UNHEALTHY

from health.recovery import RecoveryManager


def test_recovery_detects_missing_replica():

    recovery = RecoveryManager()

    result = recovery.needs_recovery(
        desired_replicas=3,
        healthy_replicas=2
    )

    assert result is True


def test_recovery_calculates_missing_replicas():

    recovery = RecoveryManager()

    result = recovery.calculate_missing_replicas(
        desired_replicas=3,
        healthy_replicas=1
    )

    assert result == 2