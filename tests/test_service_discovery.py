from cluster.service_discovery import ServiceDiscovery
from app.runtime.docker_runtime import DockerRuntime


def test_service_discovery_finds_deployment_replicas():

    runtime = DockerRuntime()

    discovery = ServiceDiscovery(
        runtime
    )

    instances = discovery.discover(
        "payment-api"
    )

    instance_ids = [
        instance.instance_id
        for instance in instances
    ]

    assert "payment-api-1" in instance_ids
    assert "payment-api-2" in instance_ids
    assert "payment-api-3" in instance_ids