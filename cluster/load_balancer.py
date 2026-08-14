from cluster.service_registry import ServiceRegistry


class RoundRobinLoadBalancer:

    def __init__(
        self,
        registry: ServiceRegistry
    ):

        self.registry = registry

        self.counters: dict[
            str,
            int
        ] = {}

    def choose(
        self,
        service_name: str
    ):

        instances = (
            self.registry
            .get_healthy_instances(
                service_name
            )
        )

        if not instances:
            return None

        current_index = (
            self.counters.get(
                service_name,
                0
            )
        )

        selected = instances[
            current_index % len(instances)
        ]

        self.counters[
            service_name
        ] = current_index + 1

        return selected