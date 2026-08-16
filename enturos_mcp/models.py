"""Modelos Pydantic compartilhados entre várias ferramentas."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class PaginationInput(BaseModel):
    """Paginação padrão da API (limit/offset)."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    limit: Optional[int] = Field(
        default=50, description="Máximo de itens a retornar (padrão 50, máximo 100).", ge=1, le=100
    )
    offset: Optional[int] = Field(
        default=0, description="Quantidade de itens a pular, para paginação.", ge=0
    )


class SearchInput(PaginationInput):
    """Paginação + busca textual livre."""

    search: Optional[str] = Field(
        default=None, description="Texto livre para buscar (nome, email, telefone etc., conforme o recurso)."
    )


class IdInput(BaseModel):
    """Identificador de um registro."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(..., description="ID do registro, conforme retornado pela API.", min_length=1)


class IdWithDataInput(BaseModel):
    """Identificador de um registro + corpo JSON para criação/atualização."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(..., description="ID do registro, conforme retornado pela API.", min_length=1)
    data: Dict[str, Any] = Field(..., description="Corpo JSON da requisição, com os campos a gravar.")


class DataInput(BaseModel):
    """Corpo JSON livre para criação de um registro."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    data: Dict[str, Any] = Field(..., description="Corpo JSON da requisição, com os campos do novo registro.")
