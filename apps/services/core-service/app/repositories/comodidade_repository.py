from uuid import UUID

from sqlalchemy.orm import Session

from app.models.comodidade import Comodidade


class ComodidadeRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Comodidade]:
        return self.db.query(Comodidade).order_by(Comodidade.nome).all()

    def buscar_por_id(self, comodidade_id: UUID) -> Comodidade | None:
        return (
            self.db.query(Comodidade)
            .filter(Comodidade.id == comodidade_id)
            .first()
        )

    def buscar_por_nome(self, nome: str) -> Comodidade | None:
        return (
            self.db.query(Comodidade)
            .filter(Comodidade.nome == nome)
            .first()
        )

    def buscar_varias_por_id(self, ids: list[UUID]) -> list[Comodidade]:
        return (
            self.db.query(Comodidade)
            .filter(Comodidade.id.in_(ids))
            .all()
        )

    def criar(self, comodidade: Comodidade) -> Comodidade:
        self.db.add(comodidade)
        self.db.commit()
        self.db.refresh(comodidade)
        return comodidade

    def remover(self, comodidade: Comodidade) -> None:
        self.db.delete(comodidade)
        self.db.commit()
