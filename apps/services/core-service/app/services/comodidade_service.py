from uuid import UUID

from fastapi import HTTPException, status

from app.models.comodidade import Comodidade
from app.repositories.comodidade_repository import ComodidadeRepository
from app.schemas.comodidade import ComodidadeCreateSchema


class ComodidadeService:
    def __init__(self, repository: ComodidadeRepository):
        self.repository = repository

    def listar(self) -> list[Comodidade]:
        return self.repository.listar()

    def buscar_por_id(self, comodidade_id: UUID) -> Comodidade:
        comodidade = self.repository.buscar_por_id(comodidade_id)
        if comodidade is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comodidade não encontrada",
            )
        return comodidade

    def criar(self, dados: ComodidadeCreateSchema) -> Comodidade:
        existente = self.repository.buscar_por_nome(dados.nome)
        if existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma comodidade com esse nome",
            )
        comodidade = Comodidade(nome=dados.nome)
        return self.repository.criar(comodidade)

    def remover(self, comodidade_id: UUID) -> None:
        comodidade = self.buscar_por_id(comodidade_id)
        self.repository.remover(comodidade)
