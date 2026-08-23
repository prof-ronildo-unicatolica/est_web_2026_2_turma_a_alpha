from uuid import UUID

from fastapi import HTTPException, status

from app.models.hotel import Hotel
from app.repositories.cidade_repository import CidadeRepository
from app.repositories.comodidade_repository import ComodidadeRepository
from app.repositories.hotel_repository import HotelRepository
from app.schemas.hotel import HotelCreateSchema


class HotelService:
    def __init__(
        self,
        repository: HotelRepository,
        cidade_repository: CidadeRepository,
        comodidade_repository: ComodidadeRepository,
    ):
        self.repository = repository
        self.cidade_repository = cidade_repository
        self.comodidade_repository = comodidade_repository

    def listar(self) -> list[Hotel]:
        return self.repository.listar()

    def buscar_por_id(self, hotel_id: UUID) -> Hotel:
        hotel = self.repository.buscar_por_id(hotel_id)
        if hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hotel não encontrado",
            )
        return hotel

    def listar_por_cidade(self, cidade_id: UUID) -> list[Hotel]:
        return self.repository.listar_por_cidade(cidade_id)

    def _validar_cidade(self, cidade_id: UUID) -> None:
        cidade = self.cidade_repository.buscar_por_id(cidade_id)
        if cidade is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cidade informada não existe",
            )

    def criar(
        self, dados: HotelCreateSchema, comodidade_ids: list[UUID] | None = None
    ) -> Hotel:
        self._validar_cidade(dados.cidade_id)

        hotel = Hotel(
            nome=dados.nome,
            categoria_estrelas=dados.categoria_estrelas,
            cidade_id=dados.cidade_id,
        )

        if comodidade_ids:
            hotel.comodidades = self.comodidade_repository.buscar_varias_por_id(
                comodidade_ids
            )

        return self.repository.criar(hotel)

    def atualizar(
        self,
        hotel_id: UUID,
        dados: HotelCreateSchema,
        comodidade_ids: list[UUID] | None = None,
    ) -> Hotel:
        hotel = self.buscar_por_id(hotel_id)
        self._validar_cidade(dados.cidade_id)

        hotel.nome = dados.nome
        hotel.categoria_estrelas = dados.categoria_estrelas
        hotel.cidade_id = dados.cidade_id

        if comodidade_ids is not None:
            hotel.comodidades = self.comodidade_repository.buscar_varias_por_id(
                comodidade_ids
            )

        return self.repository.atualizar(hotel)

    def remover(self, hotel_id: UUID) -> None:
        hotel = self.buscar_por_id(hotel_id)
        self.repository.remover(hotel)
