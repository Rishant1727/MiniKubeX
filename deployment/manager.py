from deployment.models.deployment import (
    DeploymentSpec,
    DeploymentStatus
)

from deployment.state import DeploymentState


class DeploymentManager:

    def __init__(self):

        self.state = DeploymentState()

    def create_deployment(
        self,
        spec: DeploymentSpec
    ):

        existing = self.state.get(
            spec.name
        )

        if existing is not None:

            raise ValueError(
                f"Deployment '{spec.name}' "
                "already exists"
            )

        deployment = DeploymentStatus(
            name=spec.name,
            image=spec.image,
            replicas=spec.replicas,
            version=1,
            status="pending"
        )

        self.state.create(
            deployment
        )

        return deployment

    def get_deployment(
        self,
        name: str
    ):

        return self.state.get(name)

    def list_deployments(self):

        return self.state.list_all()