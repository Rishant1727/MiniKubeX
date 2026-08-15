import docker


class DockerRuntime:

    def __init__(self):
        self.client = docker.from_env()

    def list_containers(self):
        return self.client.containers.list(all=True)

    def create_container(
        self,
        image: str,
        name: str
    ):
        container = self.client.containers.run(
            image=image,
            name=name,
            detach=True
        )

        return container

    def ensure_image(
        self,
        image: str
    ):
        try:
            self.client.images.get(
                image
            )

        except docker.errors.ImageNotFound:

            self.client.images.pull(
                image
            )

    def stop_container(
        self,
        container_id: str
    ):
        container = self.client.containers.get(
            container_id
        )

        container.stop()

    def remove_container(
        self,
        container_id: str
    ):
        container = self.client.containers.get(
            container_id
        )

        container.remove(
            force=True
        )