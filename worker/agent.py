import platform
import socket

import psutil
from fastapi import FastAPI

from worker.docker_runtime import WorkerDockerRuntime
from health.monitor import HealthMonitor

app = FastAPI(title="MiniKubeX Worker")

WORKER_ID = socket.gethostname()

docker_runtime = WorkerDockerRuntime()
health_monitor = HealthMonitor()

@app.get("/")
def root():

    return {
        "worker_id": WORKER_ID,
        "status": "running"
    }


@app.get("/info")
def worker_info():

    memory = psutil.virtual_memory()

    return {
        "worker_id": WORKER_ID,
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": memory.total,
        "memory_available": memory.available
    }


@app.get("/containers")
def list_containers():

    return docker_runtime.list_containers()


@app.post("/containers")
def create_container(image: str, name: str):

    return docker_runtime.create_container(
        image=image,
        name=name
    )

@app.get("/health/containers")
def container_health():

    containers = docker_runtime.client.containers.list(
        all=True
    )

    results = []

    for container in containers:

        health = health_monitor.check_container(
            container
        )

        results.append(
            health.model_dump()
        )

    return results