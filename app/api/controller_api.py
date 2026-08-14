from fastapi import APIRouter

from controller.models.deployment import Deployment
from controller.reconciler import Reconciler


router = APIRouter(
    prefix="/controller",
    tags=["Controller"]
)

reconciler = Reconciler()


@router.post("/reconcile")
def reconcile_deployment(
    deployment: Deployment,
    actual_replicas: int
):

    result = reconciler.reconcile(
        deployment,
        actual_replicas
    )

    return {
        "deployment": deployment.name,
        "desired_replicas": deployment.replicas,
        "actual_replicas": actual_replicas,
        "reconciliation": result
    }