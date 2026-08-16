"""Ferramentas de Tags do EnturOS CRM."""

from typing import List

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_delete, api_get, api_post
from ..core import mcp
from ..utils import run_tool


class ContactTagsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(..., description="ID do contato.", min_length=1)
    tags: List[str] = Field(..., description="Lista de nomes de tags.", min_length=1)


@mcp.tool(
    name="entur_add_contact_tags",
    annotations={
        "title": "Aplicar tag(s) no contato",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_add_contact_tags(params: ContactTagsInput) -> str:
    """Aplica uma ou mais tags a um contato. Tags inexistentes são criadas automaticamente.

    Args:
        params (ContactTagsInput): id do contato + tags (lista de nomes).

    Returns:
        str: JSON com o resultado, ou mensagem de erro.
    """
    return await run_tool(api_post(f"/contacts/{params.id}/tags", {"tags": params.tags}))


@mcp.tool(
    name="entur_remove_contact_tags",
    annotations={
        "title": "Remover tag(s) do contato",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_remove_contact_tags(params: ContactTagsInput) -> str:
    """Remove uma ou mais tags de um contato (a tag em si continua existindo na empresa).

    Args:
        params (ContactTagsInput): id do contato + tags (lista de nomes a remover).

    Returns:
        str: JSON com o resultado, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/contacts/{params.id}/tags", {"tags": params.tags}))


class RemoveSingleTagInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(..., description="ID do contato.", min_length=1)
    name: str = Field(..., description="Nome da tag a remover.", min_length=1)


@mcp.tool(
    name="entur_remove_contact_tag",
    annotations={
        "title": "Remover uma tag específica do contato",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_remove_contact_tag(params: RemoveSingleTagInput) -> str:
    """Remove uma única tag, pelo nome, de um contato.

    Args:
        params (RemoveSingleTagInput): id do contato + name (nome exato da tag).

    Returns:
        str: JSON com o resultado, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/contacts/{params.id}/tags/{params.name}"))


@mcp.tool(
    name="entur_list_tags",
    annotations={
        "title": "Listar tags da empresa",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_tags() -> str:
    """Lista todas as tags já criadas na empresa.

    Returns:
        str: JSON com a lista de tags.
    """
    return await run_tool(api_get("/tags"))
