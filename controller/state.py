from typing import Dict, List


class ClusterState:

    def __init__(self):

        self.containers: Dict[
            str,
            List[dict]
        ] = {}

    def add_container(
        self,
        deployment_name: str,
        container_id: str,
        healthy: bool = True
    ):

        if deployment_name not in self.containers:

            self.containers[
                deployment_name
            ] = []

        self.containers[
            deployment_name
        ].append(
            {
                "id": container_id,
                "healthy": healthy
            }
        )

    def remove_container(
        self,
        deployment_name: str,
        container_id: str
    ):

        if deployment_name not in self.containers:
            return

        self.containers[
            deployment_name
        ] = [

            container

            for container
            in self.containers[
                deployment_name
            ]

            if container["id"] != container_id
        ]

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

    def get_healthy_replica_count(
        self,
        deployment_name: str
    ) -> int:

        return sum(

            1

            for container
            in self.containers.get(
                deployment_name,
                []
            )

            if container["healthy"]
        )