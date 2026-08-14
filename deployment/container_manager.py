import docker


class ContainerManager:

    def __init__(self):

        self.client = docker.from_env()

    def create_container(
        self,
        deployment_name: str,
        image: str,
        version: int,
        replica: int
    ):

        name = (
            f"minikubex-"
            f"{deployment_name}-"
            f"v{version}-"
            f"{replica}"
        )

        container = self.client.containers.run(
            image=image,
            name=name,
            detach=True
        )

        return {
            "id": container.id,
            "name": container.name,
            "status": container.status
        }

    def stop_container(
        self,
        container_id: str
    ):

        container = (
            self.client
            .containers
            .get(container_id)
        )

        container.stop()

    def remove_container(
        self,
        container_id: str
    ):

        container = (
            self.client
            .containers
            .get(container_id)
        )

        container.remove(
            force=True
        )

    def get_deployment_containers(
        self,
        deployment_name: str
    ):

        containers = (
            self.client
            .containers
            .list(
                all=True
            )
        )

        prefix = (
            f"minikubex-"
            f"{deployment_name}-"
        )

        return [
            container

            for container
            in containers

            if container.name.startswith(
                prefix
            )
        ]