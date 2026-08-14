from health.models.status import (
    ContainerHealth,
    HealthStatus
)


class HealthMonitor:

    def check_container(
        self,
        container
    ) -> ContainerHealth:

        if container.status == "running":

            return ContainerHealth(
                container_id=container.id,
                name=container.name,
                status=HealthStatus.HEALTHY
            )

        return ContainerHealth(
            container_id=container.id,
            name=container.name,
            status=HealthStatus.UNHEALTHY
        )