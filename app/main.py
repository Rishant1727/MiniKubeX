import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.runtime.docker_runtime import DockerRuntime

from app.api.scheduler_api import (
    router as scheduler_router
)

from app.api.controller_api import (
    router as controller_router
)

from app.api.cluster_api import (
    router as cluster_router
)

from app.api.service_api import (
    router as service_router
)

from app.api.deployment_api import (
    router as deployment_router
)

from app.api.cluster_api import registry

from app.api.deployment_api import (
    manager,
    executor
)

from app.api.service_api import (
    service_registry,
    service_controller
)


app = FastAPI(
    title="MiniKubeX",
    description="Kubernetes-inspired container orchestrator",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


runtime = DockerRuntime()


# -------------------------------------------------
# Worker health monitor
# -------------------------------------------------

async def worker_health_monitor():

    while True:

        try:

            registry.check_worker_health()

        except Exception as error:

            print(
                f"Worker health monitor error: {error}"
            )

        await asyncio.sleep(5)


# -------------------------------------------------
# Deployment reconciliation monitor
# -------------------------------------------------

async def deployment_reconciliation_monitor():

    while True:

        try:

            deployments = (
                manager.list_deployments()
            )

            for deployment in deployments:

                # -----------------------------------------
                # Check current Docker state
                # -----------------------------------------

                state = executor.get_current_state(
                    deployment.name
                )

                healthy_replicas = (
                    state["healthy_replicas"]
                )

                needs_reconciliation = (
                    state["replicas"]
                    != deployment.replicas
                    or
                    healthy_replicas
                    != deployment.replicas
                )

                # -----------------------------------------
                # Reconcile deployment if necessary
                # -----------------------------------------

                if needs_reconciliation:

                    execution = executor.execute(
                        deployment_name=deployment.name,
                        image=deployment.image,
                        replicas=deployment.replicas
                    )

                    healthy_replicas = (
                        execution[
                            "healthy_replicas"
                        ]
                    )

                    deployment.available_replicas = (
                        healthy_replicas
                    )

                    if (
                        healthy_replicas
                        == deployment.replicas
                    ):

                        deployment.status = (
                            "running"
                        )

                    else:

                        deployment.status = (
                            "updating"
                        )

                    manager.state.update(
                        deployment
                    )

                # -----------------------------------------
                # Synchronize associated service
                # -----------------------------------------

                for service in (
                    service_registry.services.values()
                ):

                    if (
                        service.deployment_name
                        != deployment.name
                    ):
                        continue

                    service_controller.sync_service(
                        service_name=service.name,
                        deployment_name=deployment.name
                    )

        except Exception as error:

            print(
                "Deployment reconciliation "
                f"error: {error}"
            )

        await asyncio.sleep(5)


# -------------------------------------------------
# Start background monitors
# -------------------------------------------------

@app.on_event("startup")
async def startup_event():

    asyncio.create_task(
        worker_health_monitor()
    )

    asyncio.create_task(
        deployment_reconciliation_monitor()
    )


# -------------------------------------------------
# Routers
# -------------------------------------------------

app.include_router(
    scheduler_router
)

app.include_router(
    controller_router
)

app.include_router(
    cluster_router
)

app.include_router(
    service_router
)

app.include_router(
    deployment_router
)


# -------------------------------------------------
# Root
# -------------------------------------------------

@app.get("/")
def root():

    return {
        "name": "MiniKubeX",
        "status": "running"
    }


# -------------------------------------------------
# Containers
# -------------------------------------------------

@app.get("/containers")
def list_containers():

    containers = (
        runtime.list_containers()
    )

    return [

        {
            "id": container.id,
            "name": container.name,
            "status": container.status
        }

        for container
        in containers
    ]