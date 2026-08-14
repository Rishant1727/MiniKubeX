from cluster.models.service import (
    Service,
    ServiceInstance
)


class ServiceRegistry:

    def __init__(self):

        self.services: dict[
            str,
            Service
        ] = {}

    def register_service(
        self,
        service: Service
    ):

        self.services[
            service.name
        ] = service

    def add_instance(
        self,
        service_name: str,
        instance: ServiceInstance
    ):

        if service_name not in self.services:

            self.services[
                service_name
            ] = Service(
                name=service_name
            )

        self.services[
            service_name
        ].instances.append(
            instance
        )

    def get_service(
        self,
        service_name: str
    ):

        return self.services.get(
            service_name
        )

    def get_healthy_instances(
        self,
        service_name: str
    ):

        service = self.get_service(
            service_name
        )

        if service is None:
            return []

        return [
            instance

            for instance
            in service.instances

            if instance.healthy
        ]