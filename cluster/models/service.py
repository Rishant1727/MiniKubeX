from pydantic import BaseModel


class ServiceInstance(BaseModel):
    instance_id: str
    host: str
    port: int
    healthy: bool = True


class Service(BaseModel):
    name: str
    instances: list[ServiceInstance] = []