from pydantic import BaseModel


class Deployment(BaseModel):
    name: str
    image: str
    replicas: int

    cpu_request: float = 1
    memory_request: float = 1