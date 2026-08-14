class ClusterState:

    def __init__(self):
        self.containers = {}

    def add_container(
        self,
        deployment_name: str,
        container_id: str
    ):

        if deployment_name not in self.containers:
            self.containers[deployment_name] = []

        self.containers[deployment_name].append(
            container_id
        )

    def remove_container(
        self,
        deployment_name: str,
        container_id: str
    ):

        if deployment_name not in self.containers:
            return

        if container_id in self.containers[deployment_name]:
            self.containers[deployment_name].remove(
                container_id
            )

    def get_replica_count(
        self,
        deployment_name: str
    ) -> int:

        return len(
            self.containers.get(
                deployment_name,
                []
            )
        )