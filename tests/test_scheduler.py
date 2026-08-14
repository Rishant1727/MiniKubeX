from scheduler.scheduler import Scheduler
from scheduler.models.node import Node
from scheduler.models.workload import Workload

def test_scheduler_selects_suitable_node():

    nodes = [

        Node(
            id="worker-1",
            cpu_capacity=8,
            memory_capacity=16,
            cpu_used=7,
            memory_used=8
        ),

        Node(
            id="worker-2",
            cpu_capacity=8,
            memory_capacity=16,
            cpu_used=2,
            memory_used=4
        ),

        Node(
            id="worker-3",
            cpu_capacity=4,
            memory_capacity=8,
            cpu_used=3,
            memory_used=7
        )
    ]

    workload = Workload(
        id="payment-api",
        image="nginx",
        cpu_request=2,
        memory_request=4
    )

    scheduler = Scheduler()

    selected = scheduler.schedule(
        nodes,
        workload
    )

    assert selected is not None
    assert selected.id == "worker-2"

def test_scheduler_returns_none_when_no_node_is_suitable():

    nodes = [

        Node(
            id="worker-1",
            cpu_capacity=4,
            memory_capacity=8,
            cpu_used=3,
            memory_used=6
        ),

        Node(
            id="worker-2",
            cpu_capacity=2,
            memory_capacity=4,
            cpu_used=1,
            memory_used=2
        )
    ]

    workload = Workload(
        id="large-api",
        image="nginx",
        cpu_request=4,
        memory_request=8
    )

    scheduler = Scheduler()

    selected = scheduler.schedule(
        nodes,
        workload
    )

    assert selected is None