from fastapi import APIRouter, HTTPException

from deployment.manager import (
    DeploymentManager
)

from deployment.models.deployment import (
    DeploymentSpec
)

from deployment.rollout import (
    RollingUpdater
)


router = APIRouter(
    prefix="/deployments",
    tags=["Deployments"]
)

manager = DeploymentManager()

updater = RollingUpdater()


@router.post("")
def create_deployment(
    spec: DeploymentSpec
):

    try:

        deployment = (
            manager
            .create_deployment(spec)
        )

        return deployment

    except ValueError as error:

        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.get("")
def list_deployments():

    return manager.list_deployments()


@router.get("/{name}")
def get_deployment(
    name: str
):

    deployment = (
        manager
        .get_deployment(name)
    )

    if deployment is None:

        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    return deployment

@router.post("/{name}/update")
def update_deployment(
    name: str,
    spec: DeploymentSpec
):

    deployment = manager.get_deployment(name)

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

    # Create a new object instead of modifying
    # the stored deployment directly.
    updated_deployment = deployment.model_copy(
        deep=True
    )

    updated_deployment.image = spec.image
    updated_deployment.replicas = spec.replicas
    updated_deployment.version = deployment.version + 1
    updated_deployment.status = "updating"

    manager.state.update(
        updated_deployment
    )

    plan = updater.create_plan(
        spec.replicas
    )

    return {
        "deployment": name,
        "old_image": deployment.image,
        "old_version": deployment.version,
        "new_image": updated_deployment.image,
        "new_version": updated_deployment.version,
        "rollout_plan": plan
    }

@router.post("/{name}/rollback")
def rollback_deployment(
    name: str
):

    deployment = (
        manager
        .get_deployment(name)
    )

    if deployment is None:

        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    result = manager.state.rollback(
        name
    )

    if result is None:

        raise HTTPException(
            status_code=400,
            detail="No previous version available"
        )

    return result