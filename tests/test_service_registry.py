from cluster.models.service import (
    Service,
    ServiceInstance
)

from cluster.service_registry import (
    ServiceRegistry
)


def test_register_service():

    registry = ServiceRegistry()

    service = Service(
        name="payment-service"
    )

    registry.register_service(
        service
    )

    result = registry.get_service(
        "payment-service"
    )

    assert result is not None
    assert result.name == "payment-service"


def test_add_service_instance():

    registry = ServiceRegistry()

    registry.register_service(
        Service(
            name="payment-service"
        )
    )

    instance = ServiceInstance(
        instance_id="payment-1",
        host="127.0.0.1",
        port=8001
    )

    registry.add_instance(
        "payment-service",
        instance
    )

    service = registry.get_service(
        "payment-service"
    )

    assert service is not None
    assert len(service.instances) == 1
    assert service.instances[0].instance_id == "payment-1"


def test_get_healthy_instances():

    registry = ServiceRegistry()

    registry.add_instance(
        "payment-service",
        ServiceInstance(
            instance_id="payment-1",
            host="127.0.0.1",
            port=8001,
            healthy=True
        )
    )

    registry.add_instance(
        "payment-service",
        ServiceInstance(
            instance_id="payment-2",
            host="127.0.0.1",
            port=8002,
            healthy=False
        )
    )

    healthy = registry.get_healthy_instances(
        "payment-service"
    )

    assert len(healthy) == 1
    assert healthy[0].instance_id == "payment-1"