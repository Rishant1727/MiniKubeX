from cluster.models.service import (
    ServiceInstance
)

from cluster.service_registry import (
    ServiceRegistry
)

from cluster.load_balancer import (
    RoundRobinLoadBalancer
)


def test_round_robin_load_balancing():

    registry = ServiceRegistry()

    registry.add_instance(
        "payment-api",
        ServiceInstance(
            instance_id="payment-1",
            host="127.0.0.1",
            port=8001
        )
    )

    registry.add_instance(
        "payment-api",
        ServiceInstance(
            instance_id="payment-2",
            host="127.0.0.1",
            port=8002
        )
    )

    registry.add_instance(
        "payment-api",
        ServiceInstance(
            instance_id="payment-3",
            host="127.0.0.1",
            port=8003
        )
    )

    load_balancer = (
        RoundRobinLoadBalancer(
            registry
        )
    )

    first = load_balancer.choose(
        "payment-api"
    )

    second = load_balancer.choose(
        "payment-api"
    )

    third = load_balancer.choose(
        "payment-api"
    )

    fourth = load_balancer.choose(
        "payment-api"
    )

    assert first.instance_id == "payment-1"
    assert second.instance_id == "payment-2"
    assert third.instance_id == "payment-3"
    assert fourth.instance_id == "payment-1"

def test_load_balancer_ignores_unhealthy_instances():

    registry = ServiceRegistry()

    registry.add_instance(
        "payment-api",
        ServiceInstance(
            instance_id="payment-1",
            host="127.0.0.1",
            port=8001,
            healthy=True
        )
    )

    registry.add_instance(
        "payment-api",
        ServiceInstance(
            instance_id="payment-2",
            host="127.0.0.1",
            port=8002,
            healthy=False
        )
    )

    load_balancer = (
        RoundRobinLoadBalancer(
            registry
        )
    )

    result = load_balancer.choose(
        "payment-api"
    )

    assert result.instance_id == (
        "payment-1"
    )