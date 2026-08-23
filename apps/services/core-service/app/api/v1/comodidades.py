from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.repositories.comodidade_repository import ComodidadeRepository
from app.schemas.comodidade import ComodidadeCreateSchema, ComodidadeResponseSchema
from app.services.comodidade_service import ComodidadeService

router = APIRouter(prefix="/comodidades", tags=["Comodidades"])


def get_comodidade_service(db: Session = Depends(get_db)) -> ComodidadeService:
    return ComodidadeService(ComodidadeRepository(db))


# --- Rota pública ---


@router.get("", response_model=list[ComodidadeResponseSchema])
def listar_comodidades(service: ComodidadeService = Depends(get_comodidade_service)):
    """Listagem pública de comodidades cadastradas."""
    return service.listar()


# --- Rotas administrativas ---


@router.post(
    "",
    response_model=ComodidadeResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def criar_comodidade(
    payload: ComodidadeCreateSchema,
    service: ComodidadeService = Depends(get_comodidade_service),
    admin: dict = Depends(get_current_admin),
):
    """Cria uma nova comodidade (somente admin)."""
    return service.criar(payload)


@router.delete("/{comodidade_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_comodidade(
    comodidade_id: UUID,
    service: ComodidadeService = Depends(get_comodidade_service),
    admin: dict = Depends(get_current_admin),
):
    """Remove uma comodidade (somente admin)."""
    service.remover(comodidade_id)
