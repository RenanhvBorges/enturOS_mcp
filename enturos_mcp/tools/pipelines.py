"""Ferramentas de Funis e Etapas do EnturOS CRM.

Cada funil tem um pipelineType: 'sales', 'pre_sale', 'post_sale', 'support', 'recovery'
ou 'custom'.
"""

from ..client import api_get
from ..core import mcp
from ..models import IdInput
from ..utils import run_tool


@mcp.tool(
    name="entur_list_pipelines",
    annotations={
        "title": "Listar funis",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_pipelines() -> str:
    """Lista todos os funis (pipelines) da empresa, com seu pipelineType.

    Returns:
        str: JSON com a lista de funis.
    """
    return await run_tool(api_get("/pipelines"))


@mcp.tool(
    name="entur_get_pipeline_stages",
    annotations={
        "title": "Ver etapas de um funil",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_pipeline_stages(params: IdInput) -> str:
    """Lista as etapas de um funil. Os campos isWon e isLost indicam as etapas de fechamento.

    Args:
        params (IdInput): id do funil (pipeline).

    Returns:
        str: JSON com a lista de etapas do funil.
    """
    return await run_tool(api_get(f"/pipelines/{params.id}/stages"))


@mcp.tool(
    name="entur_get_pipeline_playbook",
    annotations={
        "title": "Ver playbook do funil",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_pipeline_playbook(params: IdInput) -> str:
    """Retorna o playbook (guia de vendas por etapa) definido para um funil.

    Args:
        params (IdInput): id do funil (pipeline).

    Returns:
        str: JSON com o playbook do funil.
    """
    return await run_tool(api_get(f"/pipelines/{params.id}/playbook"))
