from uuid import UUID

from fastapi import HTTPException, status

from app.models.cidade import Cidade
from app.repositories.cidade_repository import CidadeRepository
from app.schemas.cidade import CidadeCreateSchema


class CidadeService:
    def __init__(self, repository: CidadeRepository):
        self.repository = repository

    def listar(self) -> list[Cidade]:
        return self.repository.listar()

    def buscar_por_id(self, cidade_id: UUID) -> Cidade:
        cidade = self.repository.buscar_por_id(cidade_id)
        if cidade is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cidade não encontrada",
            )
        return cidade

    def criar(self, dados: CidadeCreateSchema) -> Cidade:
        existente = self.repository.buscar_por_nome(dados.nome)
        if existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma cidade com esse nome",
            )
        cidade = Cidade(nome=dados.nome, estado=dados.estado.upper())
        return self.repository.criar(cidade)

    def atualizar(self, cidade_id: UUID, dados: CidadeCreateSchema) -> Cidade:
        cidade = self.buscar_por_id(cidade_id)

        if dados.nome != cidade.nome:
            existente = self.repository.buscar_por_nome(dados.nome)
            if existente is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Já existe uma cidade com esse nome",
                )

        cidade.nome = dados.nome
        cidade.estado = dados.estado.upper()
        return self.repository.atualizar(cidade)

    def remover(self, cidade_id: UUID) -> None:
        cidade = self.buscar_por_id(cidade_id)
        self.repository.remover(cidade)
