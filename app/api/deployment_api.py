from fastapi import APIRouter, HTTPException

from deployment.executor import DeploymentExecutor
from app.runtime.docker_runtime import DockerRuntime
from controller.state import ClusterState

from deployment.manager import DeploymentManager

from deployment.models.deployment import DeploymentSpec

from deployment.rollout import RollingUpdater


router = APIRouter(
    prefix="/deployments",
    tags=["Deployments"]
)


manager = DeploymentManager()

updater = RollingUpdater()

runtime = DockerRuntime()

cluster_state = ClusterState()

executor = DeploymentExecutor(
    runtime=runtime,
    cluster_state=cluster_state
)


# -------------------------------------------------
# CREATE DEPLOYMENT
# -------------------------------------------------

@router.post("")
def create_deployment(
    spec: DeploymentSpec
):

    try:

        deployment = (
            manager.create_deployment(
                spec
            )
        )

        return deployment

    except ValueError as error:

        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


# -------------------------------------------------
# LIST DEPLOYMENTS
# -------------------------------------------------

@router.get("")
def list_deployments():

    return manager.list_deployments()


# -------------------------------------------------
# GET DEPLOYMENT
# -------------------------------------------------

@router.get("/{name}")
def get_deployment(
    name: str
):

    deployment = (
        manager.get_deployment(
            name
        )
    )

    if deployment is None:

        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    return deployment


# -------------------------------------------------
# UPDATE DEPLOYMENT
# -------------------------------------------------

@router.post("/{name}/update")
def update_deployment(
    name: str,
    spec: DeploymentSpec
):

    deployment = (
        manager.get_deployment(
            name
        )
    )

    if deployment is None:

        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    if spec.name != name:

        raise HTTPException(
            status_code=400,
            detail="Deployment name mismatch"
        )

    # -------------------------------------------------
    # Create updated deployment object
    # -------------------------------------------------

    updated_deployment = (
        deployment.model_copy(
            deep=True
        )
    )

    updated_deployment.image = (
        spec.image
    )

    updated_deployment.replicas = (
        spec.replicas
    )

    updated_deployment.version = (
        deployment.version + 1
    )

    updated_deployment.status = (
        "updating"
    )

    # -------------------------------------------------
    # Create rolling update plan
    # -------------------------------------------------

    plan = updater.create_plan(
        spec.replicas
    )

    # -------------------------------------------------
    # Execute update on Docker
    #
    # IMPORTANT:
    # State is NOT saved until Docker execution
    # succeeds.
    # -------------------------------------------------

    try:

        execution = executor.execute(
            deployment_name=name,
            image=spec.image,
            replicas=spec.replicas
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=(
                "Deployment update failed: "
                f"{error}"
            )
        )

    # -------------------------------------------------
    # Update replica information
    # -------------------------------------------------

    updated_deployment.available_replicas = (
        execution[
            "healthy_replicas"
        ]
    )

    if (
        updated_deployment.available_replicas
        == updated_deployment.replicas
    ):

        updated_deployment.status = (
            "running"
        )

    else:

        updated_deployment.status = (
            "updating"
        )

    # -------------------------------------------------
    # Save ONLY after successful execution
    # -------------------------------------------------

    manager.state.update(
        updated_deployment
    )

    # -------------------------------------------------
    # Return result
    # -------------------------------------------------

    return {

        "deployment": name,

        "old_image":
            deployment.image,

        "old_version":
            deployment.version,

        "new_image":
            updated_deployment.image,

        "new_version":
            updated_deployment.version,

        "rollout_plan":
            plan,

        "execution":
            execution
    }


# -------------------------------------------------
# ROLLBACK DEPLOYMENT
# -------------------------------------------------

@router.post("/{name}/rollback")
def rollback_deployment(
    name: str
):

    deployment = (
        manager.get_deployment(
            name
        )
    )

    if deployment is None:

        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    # -------------------------------------------------
    # Restore previous version
    # -------------------------------------------------

    result = (
        manager.state.rollback(
            name
        )
    )

    if result is None:

        raise HTTPException(
            status_code=400,
            detail="No previous version available"
        )

    # -------------------------------------------------
    # Execute rollback on Docker
    # -------------------------------------------------

    try:

        execution = executor.execute(
            deployment_name=name,
            image=result.image,
            replicas=result.replicas
        )

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=(
                "Rollback failed: "
                f"{error}"
            )
        )

    # -------------------------------------------------
    # Update actual replica information
    # -------------------------------------------------

    result.available_replicas = (
        execution[
            "healthy_replicas"
        ]
    )

    if (
        result.available_replicas
        == result.replicas
    ):

        result.status = (
            "running"
        )

    else:

        result.status = (
            "updating"
        )

    # -------------------------------------------------
    # Do NOT call manager.state.update(result)
    #
    # rollback() already saved the restored state.
    # -------------------------------------------------

    return {

        "deployment": name,

        "image":
            result.image,

        "version":
            result.version,

        "replicas":
            result.replicas,

        "available_replicas":
            result.available_replicas,

        "status":
            result.status,

        "execution":
            execution
    }