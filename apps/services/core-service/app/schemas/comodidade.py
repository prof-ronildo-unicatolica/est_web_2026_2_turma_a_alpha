from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ComodidadeBaseSchema(BaseModel):
    nome: str


class ComodidadeCreateSchema(ComodidadeBaseSchema):
    pass


class ComodidadeResponseSchema(ComodidadeBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
