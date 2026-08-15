from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class DeploymentDB(Base):

    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    image: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    replicas: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )