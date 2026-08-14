from fastapi import FastAPI
from app.runtime.docker_runtime import DockerRuntime


app = FastAPI(
    title="MiniKubeX",
    description="Kubernetes-inspired container orchestrator",
    version="0.1.0"
)

runtime = DockerRuntime()


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