from database.connection import Base, engine

from database.models.deployment import (
    DeploymentDB
)


def init_database():

    Base.metadata.create_all(
        bind=engine
    )