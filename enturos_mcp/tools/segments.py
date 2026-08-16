"""Ferramentas de Segmentos / audiências do EnturOS CRM."""

from ..client import api_get, api_post
from ..core import mcp
from ..models import DataInput
from ..utils import run_tool


@mcp.tool(
    name="entur_list_segments",
    annotations={
        "title": "Listar segmentos",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_segments() -> str:
    """Lista os segmentos (audiências) já criados na empresa.

    Returns:
        str: JSON com a lista de segmentos.
    """
    return await run_tool(api_get("/segments"))


@mcp.tool(
    name="entur_create_segment",
    annotations={
        "title": "Criar segmento",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_segment(params: DataInput) -> str:
    """Cria um novo segmento (audiência) a partir de uma definição de regras. Recomenda-se
    rodar entur_preview_segment_audience antes, com as mesmas regras, para conferir contagem
    e amostra.

    Args:
        params (DataInput): data (dict) com os campos do segmento. Campos típicos: name
            (obrigatório), rules (dict com os critérios de filtro).

    Returns:
        str: JSON do segmento criado.
    """
    return await run_tool(api_post("/segments", params.data))


@mcp.tool(
    name="entur_preview_segment_audience",
    annotations={
        "title": "Preview de audiência de segmento",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_preview_segment_audience(params: DataInput) -> str:
    """Simula uma definição de regras de segmento, sem criar nada, retornando a contagem
    de contatos que se encaixam e uma amostra deles.

    Args:
        params (DataInput): data (dict) com "rules" (os critérios de filtro a testar).

    Returns:
        str: JSON com a contagem total e uma amostra de contatos que atendem às regras.
    """
    return await run_tool(api_post("/segments/preview", params.data))
