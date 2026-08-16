"""Ferramentas de Catálogos de configuração do EnturOS CRM.

Motivos de perda, rótulos de tipo de produto e segmentos de conta (B2B). CRUD com
arquivamento reversível.
"""

from ..client import api_delete, api_get, api_patch, api_post
from ..core import mcp
from ..models import DataInput, IdInput, IdWithDataInput
from ..utils import run_tool

# --- Motivos de perda (mutações; leitura fica em entur_list_loss_reasons, tools/deals.py) ---


@mcp.tool(
    name="entur_create_loss_reason",
    annotations={
        "title": "Criar motivo de perda",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_loss_reason(params: DataInput) -> str:
    """Cria um novo motivo de perda, disponível para uso ao marcar negociações como perdidas.

    Args:
        params (DataInput): data (dict) com os campos do motivo. Campos típicos: name
            (obrigatório), pipelineId ou pipelineType (para restringir a um funil/tipo).

    Returns:
        str: JSON do motivo de perda criado.
    """
    return await run_tool(api_post("/loss-reasons", params.data))


@mcp.tool(
    name="entur_update_loss_reason",
    annotations={
        "title": "Editar motivo de perda",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_loss_reason(params: IdWithDataInput) -> str:
    """Edita um motivo de perda existente.

    Args:
        params (IdWithDataInput): id do motivo de perda + data (dict) com os campos a alterar.

    Returns:
        str: JSON do motivo de perda atualizado.
    """
    return await run_tool(api_patch(f"/loss-reasons/{params.id}", params.data))


@mcp.tool(
    name="entur_archive_loss_reason",
    annotations={
        "title": "Arquivar motivo de perda",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_archive_loss_reason(params: IdInput) -> str:
    """Arquiva (soft-delete reversível) um motivo de perda.

    Args:
        params (IdInput): id do motivo de perda a arquivar.

    Returns:
        str: JSON de confirmação, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/loss-reasons/{params.id}"))


@mcp.tool(
    name="entur_restore_loss_reason",
    annotations={
        "title": "Restaurar motivo de perda",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_restore_loss_reason(params: IdInput) -> str:
    """Restaura um motivo de perda previamente arquivado.

    Args:
        params (IdInput): id do motivo de perda a restaurar.

    Returns:
        str: JSON do motivo de perda restaurado.
    """
    return await run_tool(api_post(f"/loss-reasons/{params.id}/restore"))


# --- Rótulos de tipo de produto ---


@mcp.tool(
    name="entur_list_product_type_labels",
    annotations={
        "title": "Listar rótulos de tipo de produto",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_product_type_labels() -> str:
    """Lista os rótulos de tipo de produto cadastrados na empresa.

    Returns:
        str: JSON com a lista de rótulos.
    """
    return await run_tool(api_get("/product-type-labels"))


@mcp.tool(
    name="entur_create_product_type_label",
    annotations={
        "title": "Criar rótulo de tipo de produto",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_product_type_label(params: DataInput) -> str:
    """Cria um novo rótulo de tipo de produto.

    Args:
        params (DataInput): data (dict) com os campos do rótulo. Campo típico: name (obrigatório).

    Returns:
        str: JSON do rótulo criado.
    """
    return await run_tool(api_post("/product-type-labels", params.data))


@mcp.tool(
    name="entur_update_product_type_label",
    annotations={
        "title": "Editar rótulo de tipo de produto",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_product_type_label(params: IdWithDataInput) -> str:
    """Edita um rótulo de tipo de produto existente.

    Args:
        params (IdWithDataInput): id do rótulo + data (dict) com os campos a alterar.

    Returns:
        str: JSON do rótulo atualizado.
    """
    return await run_tool(api_patch(f"/product-type-labels/{params.id}", params.data))


@mcp.tool(
    name="entur_archive_product_type_label",
    annotations={
        "title": "Arquivar rótulo de tipo de produto",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_archive_product_type_label(params: IdInput) -> str:
    """Arquiva (soft-delete reversível) um rótulo de tipo de produto.

    Args:
        params (IdInput): id do rótulo a arquivar.

    Returns:
        str: JSON de confirmação, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/product-type-labels/{params.id}"))


@mcp.tool(
    name="entur_restore_product_type_label",
    annotations={
        "title": "Restaurar rótulo de tipo de produto",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_restore_product_type_label(params: IdInput) -> str:
    """Restaura um rótulo de tipo de produto previamente arquivado.

    Args:
        params (IdInput): id do rótulo a restaurar.

    Returns:
        str: JSON do rótulo restaurado.
    """
    return await run_tool(api_post(f"/product-type-labels/{params.id}/restore"))


# --- Segmentos de conta (B2B) ---


@mcp.tool(
    name="entur_list_account_segments",
    annotations={
        "title": "Listar segmentos de conta",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_account_segments() -> str:
    """Lista os segmentos de conta (B2B) cadastrados na empresa.

    Returns:
        str: JSON com a lista de segmentos de conta.
    """
    return await run_tool(api_get("/account-segments"))


@mcp.tool(
    name="entur_create_account_segment",
    annotations={
        "title": "Criar segmento de conta",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_account_segment(params: DataInput) -> str:
    """Cria um novo segmento de conta (B2B).

    Args:
        params (DataInput): data (dict) com os campos do segmento. Campo típico: name (obrigatório).

    Returns:
        str: JSON do segmento de conta criado.
    """
    return await run_tool(api_post("/account-segments", params.data))


@mcp.tool(
    name="entur_update_account_segment",
    annotations={
        "title": "Editar segmento de conta",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_account_segment(params: IdWithDataInput) -> str:
    """Edita um segmento de conta (B2B) existente.

    Args:
        params (IdWithDataInput): id do segmento + data (dict) com os campos a alterar.

    Returns:
        str: JSON do segmento de conta atualizado.
    """
    return await run_tool(api_patch(f"/account-segments/{params.id}", params.data))


@mcp.tool(
    name="entur_archive_account_segment",
    annotations={
        "title": "Arquivar segmento de conta",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_archive_account_segment(params: IdInput) -> str:
    """Arquiva (soft-delete reversível) um segmento de conta (B2B).

    Args:
        params (IdInput): id do segmento a arquivar.

    Returns:
        str: JSON de confirmação, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/account-segments/{params.id}"))


@mcp.tool(
    name="entur_restore_account_segment",
    annotations={
        "title": "Restaurar segmento de conta",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_restore_account_segment(params: IdInput) -> str:
    """Restaura um segmento de conta (B2B) previamente arquivado.

    Args:
        params (IdInput): id do segmento a restaurar.

    Returns:
        str: JSON do segmento de conta restaurado.
    """
    return await run_tool(api_post(f"/account-segments/{params.id}/restore"))
