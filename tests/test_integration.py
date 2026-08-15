from deployment.executor import DeploymentExecutor

from controller.state import ClusterState

from cluster.service_controller import (
    ServiceController
)

from cluster.service_registry import (
    ServiceRegistry
)

from cluster.load_balancer import (
    RoundRobinLoadBalancer
)

from cluster.models.service import (
    ServiceInstance
)


class FakeContainer:

    def __init__(
        self,
        name: str
    ):
        self.name = name
        self.id = f"id-{name}"
        self.status = "running"

        self.image = FakeImage(
            "nginx:alpine"
        )

    def reload(self):
        pass


class FakeImage:

    def __init__(
        self,
        tag: str
    ):
        self.tags = [tag]


class FakeRuntime:

    def __init__(self):

        self.containers = [
            FakeContainer(
                "payment-api-1"
            ),
            FakeContainer(
                "payment-api-2"
            ),
            FakeContainer(
                "payment-api-3"
            )
        ]

    def ensure_image(
        self,
        image: str
    ):
        pass

    def list_containers(self):

        return self.containers


def test_deployment_to_service_to_load_balancer():

    # -------------------------------------------------
    # Deployment / Docker layer
    # -------------------------------------------------

    runtime = FakeRuntime()

    cluster_state = ClusterState()

    executor = DeploymentExecutor(
        runtime=runtime,
        cluster_state=cluster_state
    )

    execution = executor.execute(
        deployment_name="payment-api",
        image="nginx:alpine",
        replicas=3
    )

    assert execution[
        "replicas"
    ] == 3

    assert execution[
        "healthy_replicas"
    ] == 3

    # -------------------------------------------------
    # Service discovery / registry
    # -------------------------------------------------

    registry = ServiceRegistry()

    service_controller = ServiceController(
        runtime=runtime,
        registry=registry
    )

    service = service_controller.sync_service(
        service_name="payment-service",
        deployment_name="payment-api"
    )

    assert service.name == (
        "payment-service"
    )

    assert service.deployment_name == (
        "payment-api"
    )

    assert len(
        service.instances
    ) == 3

    # -------------------------------------------------
    # Verify discovered instances
    # -------------------------------------------------

    instance_ids = [
        instance.instance_id
        for instance in service.instances
    ]

    assert "payment-api-1" in instance_ids
    assert "payment-api-2" in instance_ids
    assert "payment-api-3" in instance_ids

    # -------------------------------------------------
    # Load balancer
    # -------------------------------------------------

    load_balancer = (
        RoundRobinLoadBalancer(
            registry
        )
    )

    first = load_balancer.choose(
        "payment-service"
    )

    second = load_balancer.choose(
        "payment-service"
    )

    third = load_balancer.choose(
        "payment-service"
    )

    assert first is not None
    assert second is not None
    assert third is not None

    assert {
        first.instance_id,
        second.instance_id,
        third.instance_id
    } == {
        "payment-api-1",
        "payment-api-2",
        "payment-api-3"
    }