import uuid

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base


class Cidade(Base):
    __tablename__ = "cidades"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    estado: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    hoteis: Mapped[List["Hotel"]] = relationship(
        back_populates="cidade",
        cascade="all, delete-orphan",
    )
