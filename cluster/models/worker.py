from datetime import datetime

from pydantic import BaseModel


class WorkerNode(BaseModel):
    worker_id: str
    host: str
    port: int

    cpu_capacity: float
    memory_capacity: float

    healthy: bool = True
    last_heartbeat: datetime | None = None