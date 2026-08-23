from uuid import UUID

from sqlalchemy.orm import Session

from app.models.cidade import Cidade


class CidadeRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Cidade]:
        return self.db.query(Cidade).order_by(Cidade.nome).all()

    def buscar_por_id(self, cidade_id: UUID) -> Cidade | None:
        return (
            self.db.query(Cidade)
            .filter(Cidade.id == cidade_id)
            .first()
        )

    def buscar_por_nome(self, nome: str) -> Cidade | None:
        return (
            self.db.query(Cidade)
            .filter(Cidade.nome == nome)
            .first()
        )

    def criar(self, cidade: Cidade) -> Cidade:
        self.db.add(cidade)
        self.db.commit()
        self.db.refresh(cidade)
        return cidade

    def atualizar(self, cidade: Cidade) -> Cidade:
        self.db.commit()
        self.db.refresh(cidade)
        return cidade

    def remover(self, cidade: Cidade) -> None:
        self.db.delete(cidade)
        self.db.commit()
