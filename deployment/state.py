import json

from deployment.models.deployment import (
    DeploymentStatus
)

from cache.redis_client import (
    redis_client,
    set_value,
    get_value,
    delete_value
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

        # Restore saved deployments
        self._load_deployments()

    # -------------------------------------------------
    # Load deployments from Redis
    # -------------------------------------------------

    def _load_deployments(self):

        keys = redis_client.keys(
            "deployment:*:data"
        )

        for key in keys:

            data = get_value(key)

            if data is None:
                continue

            try:

                deployment_data = json.loads(
                    data
                )

                deployment = DeploymentStatus(
                    **deployment_data
                )

                self.deployments[
                    deployment.name
                ] = deployment

            except Exception as error:

                print(
                    f"Failed to restore deployment "
                    f"{key}: {error}"
                )

        # Restore rollback history
        history_keys = redis_client.keys(
            "deployment:*:history"
        )

        for key in history_keys:

            data = get_value(key)

            if data is None:
                continue

            try:

                name = key[
                    len("deployment:"):
                    -len(":history")
                ]

                self.previous_versions[
                    name
                ] = json.loads(data)

            except Exception as error:

                print(
                    f"Failed to restore history "
                    f"{key}: {error}"
                )

        # Make sure every deployment has history
        for name in self.deployments:

            self.previous_versions.setdefault(
                name,
                []
            )

    # -------------------------------------------------
    # Save deployment
    # -------------------------------------------------

    def _save_deployment(
        self,
        deployment: DeploymentStatus
    ):

        set_value(
            f"deployment:{deployment.name}:data",
            json.dumps(
                deployment.model_dump(
                    mode="json"
                )
            )
        )

    # -------------------------------------------------
    # Save rollback history
    # -------------------------------------------------

    def _save_history(
        self,
        name: str
    ):

        set_value(
            f"deployment:{name}:history",
            json.dumps(
                self.previous_versions.get(
                    name,
                    []
                )
            )
        )

    # -------------------------------------------------
    # Create deployment
    # -------------------------------------------------

    def create(
        self,
        deployment: DeploymentStatus
    ):

        saved_deployment = (
            deployment.model_copy(
                deep=True
            )
        )

        self.deployments[
            deployment.name
        ] = saved_deployment

        self.previous_versions[
            deployment.name
        ] = []

        self._save_deployment(
            saved_deployment
        )

        self._save_history(
            deployment.name
        )

    # -------------------------------------------------
    # Get deployment
    # -------------------------------------------------

    def get(
        self,
        name: str
    ):

        return self.deployments.get(
            name
        )

    # -------------------------------------------------
    # Update deployment
    # -------------------------------------------------

    def update(
        self,
        deployment: DeploymentStatus
    ):

        existing = self.get(
            deployment.name
        )

        if existing:

            self.previous_versions.setdefault(
                deployment.name,
                []
            )

            self.previous_versions[
                deployment.name
            ].append(
                {
                    "image": existing.image,
                    "version": existing.version,
                    "replicas": existing.replicas
                }
            )

            self._save_history(
                deployment.name
            )

        saved_deployment = (
            deployment.model_copy(
                deep=True
            )
        )

        self.deployments[
            deployment.name
        ] = saved_deployment

        self._save_deployment(
            saved_deployment
        )

    # -------------------------------------------------
    # Rollback
    # -------------------------------------------------

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

        deployment = self.get(
            name
        )

        if deployment is None:
            return None

        deployment.image = previous[
            "image"
        ]

        deployment.version = previous[
            "version"
        ]

        deployment.replicas = previous.get(
            "replicas",
            deployment.replicas
        )

        deployment.status = "running"

        self._save_history(
            name
        )

        self._save_deployment(
            deployment
        )

        return deployment

    # -------------------------------------------------
    # Delete deployment
    # -------------------------------------------------

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

        delete_value(
            f"deployment:{name}:data"
        )

        delete_value(
            f"deployment:{name}:history"
        )

    # -------------------------------------------------
    # List deployments
    # -------------------------------------------------

    def list_all(self):

        return list(
            self.deployments.values()
        )