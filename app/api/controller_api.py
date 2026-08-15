from fastapi import APIRouter

from controller.models.deployment import Deployment
from controller.reconciler import Reconciler

from app.api.deployment_api import executor


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

    # -------------------------------------------------
    # 1. Ask the reconciler what needs to happen
    # -------------------------------------------------

    result = reconciler.reconcile(
        deployment,
        actual_replicas
    )

    # -------------------------------------------------
    # 2. No changes required
    # -------------------------------------------------

    if result["action"] == "none":

        return {
            "deployment": deployment.name,
            "desired_replicas":
                deployment.replicas,
            "actual_replicas":
                actual_replicas,
            "reconciliation":
                result
        }

    # -------------------------------------------------
    # 3. Reconcile missing replicas
    # -------------------------------------------------

    if result["action"] == "create":

        execution = executor.execute(
            deployment_name=deployment.name,
            image=deployment.image,
            replicas=deployment.replicas
        )

        return {
            "deployment": deployment.name,
            "desired_replicas":
                deployment.replicas,
            "actual_replicas":
                actual_replicas,
            "reconciliation":
                result,
            "execution":
                execution
        }

    # -------------------------------------------------
    # 4. Reconcile extra replicas
    # -------------------------------------------------

    if result["action"] == "remove":

        execution = executor.execute(
            deployment_name=deployment.name,
            image=deployment.image,
            replicas=deployment.replicas
        )

        return {
            "deployment": deployment.name,
            "desired_replicas":
                deployment.replicas,
            "actual_replicas":
                actual_replicas,
            "reconciliation":
                result,
            "execution":
                execution
        }

    # -------------------------------------------------
    # 5. Unknown action
    # -------------------------------------------------

    return {
        "deployment": deployment.name,
        "desired_replicas":
            deployment.replicas,
        "actual_replicas":
            actual_replicas,
        "reconciliation":
            result
    }