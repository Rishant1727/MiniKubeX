from pydantic import BaseModel


class DeploymentSpec(BaseModel):
    name: str
    image: str
    replicas: int

    cpu_request: float = 1
    memory_request: float = 1


class DeploymentStatus(BaseModel):
    name: str
    image: str
    replicas: int

    available_replicas: int = 0

    version: int = 1

    status: str = "pending"