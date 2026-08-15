from app.runtime.docker_runtime import DockerRuntime

from cluster.service_controller import (
    ServiceController
)

from cluster.service_registry import (
    ServiceRegistry
)

from cluster.models.service import (
    ServiceInstance
)


def test_service_controller_syncs_deployment():

    runtime = DockerRuntime()

    registry = ServiceRegistry()

    controller = ServiceController(
        runtime=runtime,
        registry=registry
    )

    service = controller.sync_service(
        service_name="payment-service",
        deployment_name="payment-api"
    )

    assert service.name == "payment-service"

    instance_ids = [
        instance.instance_id
        for instance in service.instances
    ]

    assert "payment-api-1" in instance_ids
    assert "payment-api-2" in instance_ids
    assert "payment-api-3" in instance_ids


def test_service_controller_removes_stale_instances():

    runtime = DockerRuntime()

    registry = ServiceRegistry()

    controller = ServiceController(
        runtime=runtime,
        registry=registry
    )

    # -------------------------------------------------
    # First discovery: 3 replicas
    # -------------------------------------------------

    controller.discovery.discover = lambda deployment_name: [

        ServiceInstance(
            instance_id="payment-api-1",
            host="payment-api-1",
            port=80,
            healthy=True
        ),

        ServiceInstance(
            instance_id="payment-api-2",
            host="payment-api-2",
            port=80,
            healthy=True
        ),

        ServiceInstance(
            instance_id="payment-api-3",
            host="payment-api-3",
            port=80,
            healthy=True
        )
    ]

    service = controller.sync_service(
        service_name="payment-service",
        deployment_name="payment-api"
    )

    assert len(
        service.instances
    ) == 3


    # -------------------------------------------------
    # Second discovery: replica 2 disappeared
    # -------------------------------------------------

    controller.discovery.discover = lambda deployment_name: [

        ServiceInstance(
            instance_id="payment-api-1",
            host="payment-api-1",
            port=80,
            healthy=True
        ),

        ServiceInstance(
            instance_id="payment-api-3",
            host="payment-api-3",
            port=80,
            healthy=True
        )
    ]

    service = controller.sync_service(
        service_name="payment-service",
        deployment_name="payment-api"
    )

    instance_ids = [
        instance.instance_id
        for instance in service.instances
    ]

    assert len(
        service.instances
    ) == 2

    assert "payment-api-1" in instance_ids
    assert "payment-api-3" in instance_ids
    assert "payment-api-2" not in instance_ids