from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.repositories.cidade_repository import CidadeRepository
from app.schemas.cidade import CidadeCreateSchema, CidadeResponseSchema
from app.services.cidade_service import CidadeService

router = APIRouter(prefix="/cidades", tags=["Cidades"])


def get_cidade_service(db: Session = Depends(get_db)) -> CidadeService:
    return CidadeService(CidadeRepository(db))


# --- Rota pública ---


@router.get("", response_model=list[CidadeResponseSchema])
def listar_cidades(service: CidadeService = Depends(get_cidade_service)):
    """Listagem pública de cidades cadastradas."""
    return service.listar()


# --- Rotas administrativas ---


@router.post(
    "",
    response_model=CidadeResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def criar_cidade(
    payload: CidadeCreateSchema,
    service: CidadeService = Depends(get_cidade_service),
    admin: dict = Depends(get_current_admin),
):
    """Cria uma nova cidade (somente admin)."""
    return service.criar(payload)


@router.put("/{cidade_id}", response_model=CidadeResponseSchema)
def atualizar_cidade(
    cidade_id: UUID,
    payload: CidadeCreateSchema,
    service: CidadeService = Depends(get_cidade_service),
    admin: dict = Depends(get_current_admin),
):
    """Atualiza uma cidade existente (somente admin)."""
    return service.atualizar(cidade_id, payload)


@router.delete("/{cidade_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_cidade(
    cidade_id: UUID,
    service: CidadeService = Depends(get_cidade_service),
    admin: dict = Depends(get_current_admin),
):
    """Remove uma cidade (somente admin)."""
    service.remover(cidade_id)
