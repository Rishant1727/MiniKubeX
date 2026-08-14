from fastapi import APIRouter, HTTPException

from cluster.models.service import (
    Service,
    ServiceInstance
)

from cluster.service_registry import (
    ServiceRegistry
)

from cluster.load_balancer import (
    RoundRobinLoadBalancer
)


router = APIRouter(
    prefix="/services",
    tags=["Services"]
)

service_registry = ServiceRegistry()

load_balancer = (
    RoundRobinLoadBalancer(
        service_registry
    )
)


@router.post("/register")
def register_service(
    service: Service
):

    service_registry.register_service(
        service
    )

    return {
        "status": "registered",
        "service": service.name
    }


@router.post(
    "/{service_name}/instances"
)
def add_service_instance(
    service_name: str,
    instance: ServiceInstance
):

    service_registry.add_instance(
        service_name,
        instance
    )

    return {
        "status": "registered",
        "service": service_name,
        "instance": instance.instance_id
    }


@router.get(
    "/{service_name}"
)
def get_service(
    service_name: str
):

    service = service_registry.get_service(
        service_name
    )

    if service is None:

        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service


@router.get(
    "/{service_name}/route"
)
def route_request(
    service_name: str
):

    instance = load_balancer.choose(
        service_name
    )

    if instance is None:

        raise HTTPException(
            status_code=503,
            detail="No healthy service instances"
        )

    return {
        "service": service_name,
        "instance_id": instance.instance_id,
        "host": instance.host,
        "port": instance.port
    }