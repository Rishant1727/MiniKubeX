from fastapi import APIRouter

from scheduler.scheduler import Scheduler
from scheduler.models.node import Node
from scheduler.models.workload import Workload


router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"]
)

scheduler = Scheduler()


@router.post("/schedule")
def schedule_workload(
    workload: Workload
):

    nodes = [

        Node(
            id="worker-1",
            cpu_capacity=8,
            memory_capacity=16,
            cpu_used=4,
            memory_used=6
        ),

        Node(
            id="worker-2",
            cpu_capacity=8,
            memory_capacity=16,
            cpu_used=1,
            memory_used=2
        ),

        Node(
            id="worker-3",
            cpu_capacity=4,
            memory_capacity=8,
            cpu_used=3,
            memory_used=6
        )
    ]

    selected_node = scheduler.schedule(
        nodes,
        workload
    )

    if selected_node is None:

        return {
            "status": "failed",
            "message": "No suitable worker found"
        }

    return {
        "status": "scheduled",
        "worker_id": selected_node.id
    }