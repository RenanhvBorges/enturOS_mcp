"""Ferramentas de Notas do EnturOS CRM."""

from ..client import api_get, api_post
from ..core import mcp
from ..models import DataInput, IdInput
from ..utils import run_tool


@mcp.tool(
    name="entur_get_contact_notes",
    annotations={
        "title": "Ver notas do contato",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_contact_notes(params: IdInput) -> str:
    """Lista as notas registradas em um contato.

    Args:
        params (IdInput): id do contato.

    Returns:
        str: JSON com a lista de notas do contato.
    """
    return await run_tool(api_get(f"/contacts/{params.id}/notes"))


@mcp.tool(
    name="entur_get_deal_notes",
    annotations={
        "title": "Ver notas da negociação",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_deal_notes(params: IdInput) -> str:
    """Lista as notas registradas em uma negociação.

    Args:
        params (IdInput): id da negociação.

    Returns:
        str: JSON com a lista de notas da negociação.
    """
    return await run_tool(api_get(f"/deals/{params.id}/notes"))


@mcp.tool(
    name="entur_create_note",
    annotations={
        "title": "Criar nota",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_note(params: DataInput) -> str:
    """Cria uma nota vinculada a um contato e/ou negociação.

    Args:
        params (DataInput): data (dict) com os campos da nota. Campos típicos: body
            (obrigatório, texto da nota), contactId e/ou dealId (ao menos um vínculo).

    Returns:
        str: JSON da nota criada.
    """
    return await run_tool(api_post("/notes", params.data))
