from app.runtime.docker_runtime import DockerRuntime

from cluster.models.service import (
    ServiceInstance
)


class ServiceDiscovery:

    def __init__(
        self,
        runtime: DockerRuntime
    ):

        self.runtime = runtime

    def discover(
        self,
        deployment_name: str
    ):

        instances = []

        containers = (
            self.runtime.list_containers()
        )

        for container in containers:

            if not container.name.startswith(
                f"{deployment_name}-"
            ):
                continue

            container.reload()

            healthy = (
                container.status == "running"
            )

            instances.append(
                ServiceInstance(
                    instance_id=container.name,
                    host=container.name,
                    port=80,
                    healthy=healthy
                )
            )

        return instances