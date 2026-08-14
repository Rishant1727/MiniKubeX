from pydantic import BaseModel


class Workload(BaseModel):
    id: str
    image: str

    cpu_request: float
    memory_request: float

    replicas: int = 1