from database.connection import SessionLocal
from database.models.deployment import DeploymentDB


class DeploymentRepository:

    def create(
        self,
        name: str,
        image: str,
        replicas: int,
        version: int = 1,
        status: str = "pending"
    ):

        with SessionLocal() as session:

            deployment = DeploymentDB(
                name=name,
                image=image,
                replicas=replicas,
                version=version,
                status=status
            )

            session.add(deployment)
            session.commit()
            session.refresh(deployment)

            return deployment

    def get(
        self,
        name: str
    ):

        with SessionLocal() as session:

            return (
                session.query(
                    DeploymentDB
                )
                .filter(
                    DeploymentDB.name == name
                )
                .first()
            )

    def list_all(self):

        with SessionLocal() as session:

            return session.query(
                DeploymentDB
            ).all()

    def delete(
        self,
        name: str
    ):

        with SessionLocal() as session:

            deployment = (
                session.query(
                    DeploymentDB
                )
                .filter(
                    DeploymentDB.name == name
                )
                .first()
            )

            if deployment:

                session.delete(
                    deployment
                )

                session.commit()