import uuid
from typing import List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base

# Tabela associativa N:M entre Hotel e Comodidade
hotel_comodidade = Table(
    "hotel_comodidade",
    Base.metadata,
    Column("hotel_id", ForeignKey("hoteis.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "comodidade_id",
        ForeignKey("comodidades.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Comodidade(Base):
    __tablename__ = "comodidades"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    hoteis: Mapped[List["Hotel"]] = relationship(
        secondary=hotel_comodidade,
        back_populates="comodidades",
    )
