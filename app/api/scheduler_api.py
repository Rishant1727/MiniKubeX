from fastapi import APIRouter

from scheduler.scheduler import Scheduler
from scheduler.models.node import Node
from scheduler.models.workload import Workload

from app.api.cluster_api import registry


router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"]
)

scheduler = Scheduler()


@router.post("/schedule")
def schedule_workload(
    workload: Workload
):

    # -------------------------------------------------
    # Get actual workers from WorkerRegistry
    # -------------------------------------------------

    workers = registry.get_healthy_workers()

    # -------------------------------------------------
    # Convert WorkerNode → Scheduler Node
    # -------------------------------------------------

    nodes = []

    for worker in workers:

        node = Node(
            id=worker.worker_id,

            cpu_capacity=worker.cpu_capacity,

            memory_capacity=worker.memory_capacity,

            # Scheduler currently does not have
            # persistent resource usage tracking,
            # so start with zero usage.
            cpu_used=0,

            memory_used=0
        )

        nodes.append(node)

    # -------------------------------------------------
    # Schedule workload
    # -------------------------------------------------

    selected_node = scheduler.schedule(
        nodes,
        workload
    )

    if selected_node is None:

        return {
            "status": "failed",
            "message": "No suitable healthy worker found"
        }

    return {
        "status": "scheduled",
        "worker_id": selected_node.id
    }