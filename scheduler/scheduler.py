from scheduler.models.node import Node
from scheduler.models.workload import Workload


class Scheduler:

    def filter_nodes(
        self,
        nodes: list[Node],
        workload: Workload
    ) -> list[Node]:

        suitable_nodes = []

        for node in nodes:

            if not node.healthy:
                continue

            if node.available_cpu < workload.cpu_request:
                continue

            if node.available_memory < workload.memory_request:
                continue

            suitable_nodes.append(node)

        return suitable_nodes

    def score_node(self, node: Node) -> float:

        cpu_score = (
            node.available_cpu / node.cpu_capacity
        )

        memory_score = (
            node.available_memory / node.memory_capacity
        )

        return cpu_score + memory_score

    def schedule(
        self,
        nodes: list[Node],
        workload: Workload
    ) -> Node | None:

        suitable_nodes = self.filter_nodes(
            nodes,
            workload
        )

        if not suitable_nodes:
            return None

        selected_node = max(
            suitable_nodes,
            key=self.score_node
        )

        return selected_node