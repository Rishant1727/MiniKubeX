from cluster.models.worker import WorkerNode
from cluster.registry import WorkerRegistry


def test_worker_registration():

    registry = WorkerRegistry()

    worker = WorkerNode(
        worker_id="worker-1",
        host="127.0.0.1",
        port=9001,
        cpu_capacity=8,
        memory_capacity=16
    )

    registry.register(worker)

    result = registry.get_worker(
        "worker-1"
    )

    assert result is not None
    assert result.worker_id == "worker-1"


def test_worker_heartbeat():

    registry = WorkerRegistry()

    worker = WorkerNode(
        worker_id="worker-1",
        host="127.0.0.1",
        port=9001,
        cpu_capacity=8,
        memory_capacity=16
    )

    registry.register(worker)

    result = registry.heartbeat(
        "worker-1"
    )

    assert result is True
    assert registry.get_worker(
        "worker-1"
    ).healthy is True