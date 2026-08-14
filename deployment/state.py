from deployment.models.deployment import (
    DeploymentStatus
)


class DeploymentState:

    def __init__(self):

        self.deployments: dict[
            str,
            DeploymentStatus
        ] = {}

        self.previous_versions: dict[
            str,
            list[dict]
        ] = {}

    def create(
        self,
        deployment: DeploymentStatus
    ):

        # Store a copy so future modifications
        # don't change our saved state.
        self.deployments[
            deployment.name
        ] = deployment.model_copy(
            deep=True
        )

        self.previous_versions[
            deployment.name
        ] = []

    def get(
        self,
        name: str
    ):

        return self.deployments.get(name)

    def update(
        self,
        deployment: DeploymentStatus
    ):

        existing = self.get(
            deployment.name
        )

        if existing:

            self.previous_versions[
                deployment.name
            ].append(
                {
                    "image": existing.image,
                    "version": existing.version
                }
            )

        self.deployments[
            deployment.name
        ] = deployment.model_copy(
            deep=True
        )

    def rollback(
        self,
        name: str
    ):

        history = self.previous_versions.get(
            name,
            []
        )

        if not history:
            return None

        previous = history.pop()

        deployment = self.get(name)

        if deployment is None:
            return None

        deployment.image = previous["image"]
        deployment.version = previous["version"]
        deployment.status = "running"

        return deployment

    def delete(
        self,
        name: str
    ):

        self.deployments.pop(
            name,
            None
        )

        self.previous_versions.pop(
            name,
            None
        )

    def list_all(self):

        return list(
            self.deployments.values()
        )