from app.runtime.docker_runtime import DockerRuntime

from cluster.service_registry import (
    ServiceRegistry
)

from cluster.service_discovery import (
    ServiceDiscovery
)


class ServiceController:

    def __init__(
        self,
        runtime: DockerRuntime,
        registry: ServiceRegistry
    ):

        self.registry = registry

        self.discovery = ServiceDiscovery(
            runtime
        )

    def sync_service(
        self,
        service_name: str,
        deployment_name: str
    ):

        instances = self.discovery.discover(
            deployment_name
        )

        service = (
            self.registry.get_service(
                service_name
            )
        )

        if service is None:

            from cluster.models.service import (
                Service
            )

            service = Service(
                name=service_name,
                deployment_name=deployment_name
            )

            self.registry.register_service(
                service
            )

        else:

            service.deployment_name = (
                deployment_name
            )

        # Replace current instances
        # with current Docker state.

        service.instances = instances

        return service