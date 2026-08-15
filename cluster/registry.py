import json
from datetime import datetime, timedelta

from cluster.models.worker import WorkerNode

from cache.redis_client import (
    redis_client,
    set_value,
    get_value,
    delete_value
)


class WorkerRegistry:

    HEARTBEAT_TIMEOUT = 30

    def __init__(self):

        self.workers: dict[
            str,
            WorkerNode
        ] = {}

        # Restore workers from Redis
        self._load_workers()

        # Check their health immediately
        self.check_worker_health()

    # -------------------------------------------------
    # Load workers from Redis
    # -------------------------------------------------

    def _load_workers(self):

        keys = redis_client.keys(
            "worker:*:data"
        )

        for key in keys:

            data = get_value(key)

            if data is None:
                continue

            try:

                worker_data = json.loads(
                    data
                )

                worker = WorkerNode(
                    **worker_data
                )

                self.workers[
                    worker.worker_id
                ] = worker

            except Exception as error:

                print(
                    f"Failed to restore worker "
                    f"{key}: {error}"
                )

    # -------------------------------------------------
    # Register worker
    # -------------------------------------------------

    def register(
        self,
        worker: WorkerNode
    ):

        worker.last_heartbeat = (
            datetime.now()
        )

        worker.healthy = True

        self.workers[
            worker.worker_id
        ] = worker

        self._save_worker(
            worker
        )

        # Create heartbeat key
        set_value(
            f"worker:{worker.worker_id}:heartbeat",
            worker.last_heartbeat.isoformat(),
            expiration=self.HEARTBEAT_TIMEOUT
        )

        return worker

    # -------------------------------------------------
    # Save worker
    # -------------------------------------------------

    def _save_worker(
        self,
        worker: WorkerNode
    ):

        set_value(
            f"worker:{worker.worker_id}:data",
            json.dumps(
                worker.model_dump(
                    mode="json"
                )
            )
        )

    # -------------------------------------------------
    # Unregister worker
    # -------------------------------------------------

    def unregister(
        self,
        worker_id: str
    ):

        self.workers.pop(
            worker_id,
            None
        )

        delete_value(
            f"worker:{worker_id}:data"
        )

        delete_value(
            f"worker:{worker_id}:heartbeat"
        )

    # -------------------------------------------------
    # Worker heartbeat
    # -------------------------------------------------

    def heartbeat(
        self,
        worker_id: str
    ):

        worker = self.workers.get(
            worker_id
        )

        if worker is None:
            return False

        worker.last_heartbeat = (
            datetime.now()
        )

        worker.healthy = True

        self._save_worker(
            worker
        )

        set_value(
            f"worker:{worker_id}:heartbeat",
            worker.last_heartbeat.isoformat(),
            expiration=self.HEARTBEAT_TIMEOUT
        )

        return True

    # -------------------------------------------------
    # Check worker health
    # -------------------------------------------------

    def check_worker_health(self):

        now = datetime.now()

        for worker in self.workers.values():

            if worker.last_heartbeat is None:

                worker.healthy = False

                self._save_worker(
                    worker
                )

                continue

            elapsed = (
                now
                - worker.last_heartbeat
            ).total_seconds()

            if elapsed > self.HEARTBEAT_TIMEOUT:

                worker.healthy = False

                self._save_worker(
                    worker
                )

    # -------------------------------------------------
    # Get one worker
    # -------------------------------------------------

    def get_worker(
        self,
        worker_id: str
    ):

        self.check_worker_health()

        return self.workers.get(
            worker_id
        )

    # -------------------------------------------------
    # Get all workers
    # -------------------------------------------------

    def get_workers(self):

        self.check_worker_health()

        return list(
            self.workers.values()
        )

    # -------------------------------------------------
    # Get healthy workers
    # -------------------------------------------------

    def get_healthy_workers(self):

        self.check_worker_health()

        return [
            worker

            for worker
            in self.workers.values()

            if worker.healthy
        ]