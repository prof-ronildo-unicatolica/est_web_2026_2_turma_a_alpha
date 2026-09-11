import uuid

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
