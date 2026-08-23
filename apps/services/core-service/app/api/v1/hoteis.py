from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.repositories.cidade_repository import CidadeRepository
from app.repositories.comodidade_repository import ComodidadeRepository
from app.repositories.hotel_repository import HotelRepository
from app.schemas.comodidade import ComodidadeResponseSchema
from app.schemas.hotel import HotelCreateSchema, HotelResponseSchema
from app.services.hotel_service import HotelService

router = APIRouter(prefix="/hoteis", tags=["Hoteis"])


class HotelComComodidadesSchema(HotelResponseSchema):
    comodidades: list[ComodidadeResponseSchema] = []


class HotelPayloadSchema(HotelCreateSchema):
    comodidade_ids: list[UUID] = []


def get_hotel_service(db: Session = Depends(get_db)) -> HotelService:
    return HotelService(
        HotelRepository(db),
        CidadeRepository(db),
        ComodidadeRepository(db),
    )


# --- Rota pública ---


@router.get("", response_model=list[HotelComComodidadesSchema])
def listar_hoteis(service: HotelService = Depends(get_hotel_service)):
    """Listagem pública de hotéis cadastrados."""
    return service.listar()


# --- Rotas administrativas ---


@router.post(
    "",
    response_model=HotelComComodidadesSchema,
    status_code=status.HTTP_201_CREATED,
)
def criar_hotel(
    payload: HotelPayloadSchema,
    service: HotelService = Depends(get_hotel_service),
    admin: dict = Depends(get_current_admin),
):
    """Cria um novo hotel (somente admin)."""
    return service.criar(payload, comodidade_ids=payload.comodidade_ids)


@router.put("/{hotel_id}", response_model=HotelComComodidadesSchema)
def atualizar_hotel(
    hotel_id: UUID,
    payload: HotelPayloadSchema,
    service: HotelService = Depends(get_hotel_service),
    admin: dict = Depends(get_current_admin),
):
    """Atualiza um hotel existente (somente admin)."""
    return service.atualizar(hotel_id, payload, comodidade_ids=payload.comodidade_ids)


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_hotel(
    hotel_id: UUID,
    service: HotelService = Depends(get_hotel_service),
    admin: dict = Depends(get_current_admin),
):
    """Remove um hotel (somente admin)."""
    service.remover(hotel_id)
