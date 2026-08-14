import docker


class WorkerDockerRuntime:

    def __init__(self):
        self.client = docker.from_env()

    def list_containers(self):

        containers = self.client.containers.list(all=True)

        return [
            {
                "id": container.id,
                "name": container.name,
                "status": container.status
            }
            for container in containers
        ]

    def create_container(self, image: str, name: str):

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