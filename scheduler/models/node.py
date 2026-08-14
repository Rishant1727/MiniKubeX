from pydantic import BaseModel


class Node(BaseModel):
    id: str
    cpu_capacity: float
    memory_capacity: float

    cpu_used: float = 0
    memory_used: float = 0

    healthy: bool = True

    @property
    def available_cpu(self) -> float:
        return self.cpu_capacity - self.cpu_used

    @property
    def available_memory(self) -> float:
        return self.memory_capacity - self.memory_used