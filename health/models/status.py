from enum import Enum

from pydantic import BaseModel


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class ContainerHealth(BaseModel):
    container_id: str
    name: str
    status: HealthStatus
    restart_count: int = 0