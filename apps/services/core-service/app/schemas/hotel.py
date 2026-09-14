import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CidadeCreateSchema(BaseModel):
    """O que o cliente envia em POST /cidades.

    Nao tem 'id': quem gera o identificador e o servidor.
    """

    nome: str = Field(min_length=1, max_length=100)


class CidadeResponseSchema(BaseModel):
    """O que a API devolve.

    O 'id' e obrigatorio para permitir que outros recursos,
    como Hotel, referenciem esta cidade.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class HotelCreateSchema(BaseModel):
    """O que o cliente envia em POST /hoteis.

    A cidade entra como ID, nao como objeto: assim nao ha duvida se e para
    reaproveitar uma cidade existente ou criar uma nova (e sempre reaproveitar).
    """

    nome: str = Field(min_length=1, max_length=100)
    cidade_id: uuid.UUID


class HotelResponseSchema(BaseModel):
    """O que a API devolve.

    A cidade vem ANINHADA e completa: sem isso o frontend precisaria de uma
    requisicao extra por hotel so para descobrir o nome da cidade.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    cidade: CidadeResponseSchema


class CidadeComHoteisSchema(CidadeResponseSchema):
    """Cidade com a lista de hoteis dentro. Usada so onde ela for pedida
    explicitamente -- ver a nota sobre recursao infinita no item 4."""

    hoteis: List[HotelResponseSchema] = []
