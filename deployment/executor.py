from app.runtime.docker_runtime import DockerRuntime
from controller.state import ClusterState
from deployment.rollout import RollingUpdater


class DeploymentExecutor:

    def __init__(
        self,
        runtime: DockerRuntime,
        cluster_state: ClusterState
    ):
        self.runtime = runtime
        self.cluster_state = cluster_state

        self.updater = RollingUpdater(
            max_unavailable=1
        )

    # -------------------------------------------------
    # Check current deployment state
    # -------------------------------------------------

    def get_current_state(
        self,
        deployment_name: str
    ):

        existing_containers = {}

        for container in self.runtime.list_containers():

            if container.name.startswith(
                f"{deployment_name}-"
            ):

                container.reload()

                existing_containers[
                    container.name
                ] = container

        self.cluster_state.containers[
            deployment_name
        ] = []

        for container in (
            existing_containers.values()
        ):

            healthy = (
                container.status == "running"
            )

            self.cluster_state.add_container(
                deployment_name=deployment_name,
                container_id=container.id,
                healthy=healthy
            )

        return {
            "replicas":
                self.cluster_state.get_replica_count(
                    deployment_name
                ),

            "healthy_replicas":
                self.cluster_state.get_healthy_replica_count(
                    deployment_name
                )
        }

    # -------------------------------------------------
    # Check whether deployment needs reconciliation
    # -------------------------------------------------

    def needs_reconciliation(
        self,
        deployment_name: str,
        replicas: int
    ) -> bool:

        state = self.get_current_state(
            deployment_name
        )

        return (
            state["replicas"] != replicas
            or
            state["healthy_replicas"] != replicas
        )

    # -------------------------------------------------
    # Check image
    # -------------------------------------------------

    def _container_uses_image(
        self,
        container,
        image: str
    ) -> bool:

        try:

            return image in container.image.tags

        except Exception:

            return False

    # -------------------------------------------------
    # Execute deployment
    # -------------------------------------------------

    def execute(
        self,
        deployment_name: str,
        image: str,
        replicas: int
    ):

        # -------------------------------------------------
        # 0. Validate image BEFORE modifying containers
        # -------------------------------------------------

        self.runtime.ensure_image(
            image
        )

        # -------------------------------------------------
        # 1. Discover existing Docker containers
        # -------------------------------------------------

        existing_containers = {}

        for container in self.runtime.list_containers():

            if container.name.startswith(
                f"{deployment_name}-"
            ):

                container.reload()

                existing_containers[
                    container.name
                ] = container

        # -------------------------------------------------
        # 2. Synchronize ClusterState
        # -------------------------------------------------

        self.cluster_state.containers[
            deployment_name
        ] = []

        for container in (
            existing_containers.values()
        ):

            healthy = (
                container.status == "running"
            )

            self.cluster_state.add_container(
                deployment_name=deployment_name,
                container_id=container.id,
                healthy=healthy
            )

        # -------------------------------------------------
        # 3. Check whether deployment is already correct
        # -------------------------------------------------

        all_replicas_healthy = (
            len(existing_containers) == replicas
            and all(
                container.status == "running"
                and self._container_uses_image(
                    container,
                    image
                )
                for container
                in existing_containers.values()
            )
        )

        # -------------------------------------------------
        # 4. Create rolling update plan only when needed
        # -------------------------------------------------

        if all_replicas_healthy:

            plan = []

        else:

            plan = self.updater.create_plan(
                replicas
            )

        # -------------------------------------------------
        # 5. Process replicas
        # -------------------------------------------------

        for step in plan:

            replica_number = step[
                "replica"
            ]

            container_name = (
                f"{deployment_name}-"
                f"{replica_number}"
            )

            existing = (
                existing_containers.get(
                    container_name
                )
            )

            # ---------------------------------------------
            # Replica doesn't exist OR is stopped
            # ---------------------------------------------

            if (
                existing is None
                or existing.status != "running"
            ):

                if existing is not None:

                    self.runtime.remove_container(
                        existing.id
                    )

                    self.cluster_state.remove_container(
                        deployment_name,
                        existing.id
                    )

                container = (
                    self.runtime.create_container(
                        image=image,
                        name=container_name
                    )
                )

                container.reload()

                healthy = (
                    container.status == "running"
                )

                self.cluster_state.add_container(
                    deployment_name=deployment_name,
                    container_id=container.id,
                    healthy=healthy
                )

                continue

            # ---------------------------------------------
            # Replica already has requested image
            # ---------------------------------------------

            if self._container_uses_image(
                existing,
                image
            ):

                continue

            # ---------------------------------------------
            # Replica has old image
            # ---------------------------------------------

            self.runtime.stop_container(
                existing.id
            )

            self.runtime.remove_container(
                existing.id
            )

            self.cluster_state.remove_container(
                deployment_name,
                existing.id
            )

            # ---------------------------------------------
            # Create replacement
            # ---------------------------------------------

            replacement = (
                self.runtime.create_container(
                    image=image,
                    name=container_name
                )
            )

            replacement.reload()

            healthy = (
                replacement.status == "running"
            )

            self.cluster_state.add_container(
                deployment_name=deployment_name,
                container_id=replacement.id,
                healthy=healthy
            )

        # -------------------------------------------------
        # 6. Remove extra replicas
        # -------------------------------------------------

        current_containers = (
            self.runtime.list_containers()
        )

        for container in current_containers:

            if not container.name.startswith(
                f"{deployment_name}-"
            ):

                continue

            suffix = container.name[
                len(deployment_name) + 1:
            ]

            try:

                replica_number = int(
                    suffix
                )

            except ValueError:

                continue

            if replica_number > replicas:

                self.runtime.remove_container(
                    container.id
                )

                self.cluster_state.remove_container(
                    deployment_name,
                    container.id
                )

        # -------------------------------------------------
        # 7. Return final state
        # -------------------------------------------------

        return {
            "deployment": deployment_name,

            "replicas":
                self.cluster_state.get_replica_count(
                    deployment_name
                ),

            "healthy_replicas":
                self.cluster_state.get_healthy_replica_count(
                    deployment_name
                ),

            "rollout_plan":
                plan
        }