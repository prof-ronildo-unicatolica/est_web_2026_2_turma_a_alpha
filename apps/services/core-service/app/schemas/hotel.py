from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HotelBaseSchema(BaseModel):
    nome: str
    categoria_estrelas: int = Field(ge=1, le=5)
    cidade_id: UUID


class HotelCreateSchema(HotelBaseSchema):
    pass


class HotelResponseSchema(HotelBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
