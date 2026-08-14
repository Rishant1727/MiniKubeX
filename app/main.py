from fastapi import FastAPI
from app.runtime.docker_runtime import DockerRuntime
from app.api.scheduler_api import router as scheduler_router
from app.api.controller_api import router as controller_router
from fastapi import BackgroundTasks
from app.api.cluster_api import router as cluster_router
from app.api.service_api import router as service_router

app = FastAPI(
    title="MiniKubeX",
    description="Kubernetes-inspired container orchestrator",
    version="0.1.0"
)

runtime = DockerRuntime()

app.include_router(scheduler_router)
app.include_router(controller_router)
app.include_router(cluster_router)
app.include_router(service_router)

@app.get("/")
def root():
    return {
        "name": "MiniKubeX",
        "status": "running"
    }


@app.get("/containers")
def list_containers():
    containers = runtime.list_containers()

    return [
        {
            "id": container.id,
            "name": container.name,
            "status": container.status
        }
        for container in containers
    ]