from cluster.models.service import (
    ServiceInstance
)

from cluster.service_registry import (
    ServiceRegistry
)


def test_service_instance_registration():

    registry = ServiceRegistry()

    instance = ServiceInstance(
        instance_id="payment-1",
        host="127.0.0.1",
        port=8001
    )

    registry.add_instance(
        "payment-api",
        instance
    )

    instances = (
        registry
        .get_healthy_instances(
            "payment-api"
        )
    )

    assert len(instances) == 1
    assert instances[0].instance_id == (
        "payment-1"
    )