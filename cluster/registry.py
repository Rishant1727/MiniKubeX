from datetime import datetime

from cluster.models.worker import WorkerNode


class WorkerRegistry:

    def __init__(self):
        self.workers: dict[str, WorkerNode] = {}

    def register(self, worker: WorkerNode):

        worker.last_heartbeat = datetime.now()

        self.workers[worker.worker_id] = worker

    def unregister(self, worker_id: str):

        self.workers.pop(
            worker_id,
            None
        )

    def heartbeat(self, worker_id: str):

        worker = self.workers.get(worker_id)

        if worker is None:
            return False

        worker.last_heartbeat = datetime.now()
        worker.healthy = True

        return True

    def get_worker(
        self,
        worker_id: str
    ):

        return self.workers.get(worker_id)

    def get_workers(self):

        return list(
            self.workers.values()
        )

    def get_healthy_workers(self):

        return [
            worker

            for worker
            in self.workers.values()

            if worker.healthy
        ]