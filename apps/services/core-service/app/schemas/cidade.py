from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CidadeBaseSchema(BaseModel):
    nome: str
    estado: str


class CidadeCreateSchema(CidadeBaseSchema):
    pass


class CidadeResponseSchema(CidadeBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
