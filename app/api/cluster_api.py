from fastapi import APIRouter, HTTPException

from cluster.models.worker import WorkerNode
from cluster.registry import WorkerRegistry


router = APIRouter(
    prefix="/cluster",
    tags=["Cluster"]
)

registry = WorkerRegistry()


@router.post("/workers/register")
def register_worker(
    worker: WorkerNode
):

    registry.register(worker)

    return {
        "status": "registered",
        "worker_id": worker.worker_id
    }


@router.post("/workers/{worker_id}/heartbeat")
def worker_heartbeat(
    worker_id: str
):

    success = registry.heartbeat(
        worker_id
    )

    if not success:

        raise HTTPException(
            status_code=404,
            detail="Worker not registered"
        )

    return {
        "status": "healthy",
        "worker_id": worker_id
    }


@router.get("/workers")
def list_workers():

    return registry.get_workers()