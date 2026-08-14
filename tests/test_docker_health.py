import docker

from health.monitor import HealthMonitor
from health.models.status import HealthStatus


def test_docker_container_health():

    client = docker.from_env()

    container = client.containers.run(
        "nginx",
        name="minikubex-health-test",
        detach=True
    )

    try:

        monitor = HealthMonitor()

        container.reload()

        result = monitor.check_container(
            container
        )

        assert result.status == (
            HealthStatus.HEALTHY
        )

    finally:

        container.remove(
            force=True
        )