"""Ferramentas de Webhooks de saída do EnturOS CRM."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_delete, api_get, api_patch, api_post
from ..core import mcp
from ..models import DataInput, IdInput, IdWithDataInput
from ..utils import run_tool


@mcp.tool(
    name="entur_list_webhooks",
    annotations={
        "title": "Listar webhooks",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_webhooks() -> str:
    """Lista os webhooks de saída já registrados na empresa.

    Returns:
        str: JSON com a lista de webhooks (sem o secret, que só é exibido na criação).
    """
    return await run_tool(api_get("/webhooks"))


@mcp.tool(
    name="entur_create_webhook",
    annotations={
        "title": "Registrar webhook",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_webhook(params: DataInput) -> str:
    """Registra um novo webhook de saída para receber eventos em tempo real. O secret HMAC
    para verificar a assinatura das entregas é retornado apenas nesta chamada — avise o
    usuário para guardá-lo com segurança, pois não pode ser recuperado depois.

    Args:
        params (DataInput): data (dict) com os campos do webhook. Campos obrigatórios: url
            (https), events (lista, ex: ["contact.*", "deal.won"]). Eventos disponíveis:
            contact.created, contact.updated, contact.deleted, deal.created, deal.updated,
            deal.won, deal.lost, deal.stage_changed, task.created, task.completed.

    Returns:
        str: JSON do webhook criado, incluindo o secret (mostrado uma única vez).
    """
    return await run_tool(api_post("/webhooks", params.data))


@mcp.tool(
    name="entur_get_webhook",
    annotations={
        "title": "Obter webhook por ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_webhook(params: IdInput) -> str:
    """Obtém os dados de um webhook pelo ID (sem o secret).

    Args:
        params (IdInput): id do webhook.

    Returns:
        str: JSON do webhook, ou mensagem de erro se não existir.
    """
    return await run_tool(api_get(f"/webhooks/{params.id}"))


@mcp.tool(
    name="entur_update_webhook",
    annotations={
        "title": "Atualizar webhook (pausar/retomar, eventos, url)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_webhook(params: IdWithDataInput) -> str:
    """Atualiza um webhook: pausa/retoma, muda a URL ou a lista de eventos assinados.

    Args:
        params (IdWithDataInput): id do webhook + data (dict) com os campos a alterar
            (ex: {"paused": true}, {"url": "..."}, {"events": [...]}).

    Returns:
        str: JSON do webhook atualizado.
    """
    return await run_tool(api_patch(f"/webhooks/{params.id}", params.data))


@mcp.tool(
    name="entur_delete_webhook",
    annotations={
        "title": "Revogar webhook",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_delete_webhook(params: IdInput) -> str:
    """Revoga (exclui) um webhook definitivamente. AÇÃO DESTRUTIVA: confirme com o usuário
    antes de executar.

    Args:
        params (IdInput): id do webhook a revogar.

    Returns:
        str: JSON de confirmação, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/webhooks/{params.id}"))


@mcp.tool(
    name="entur_test_webhook",
    annotations={
        "title": "Testar webhook (evento ping)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_test_webhook(params: IdInput) -> str:
    """Envia uma entrega de teste (evento ping) para o webhook, para validar se o endpoint
    do cliente está recebendo e verificando corretamente.

    Args:
        params (IdInput): id do webhook a testar.

    Returns:
        str: JSON com o resultado do envio de teste.
    """
    return await run_tool(api_post(f"/webhooks/{params.id}/test"))


class WebhookDeliveriesInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(..., description="ID do webhook.", min_length=1)
    limit: Optional[int] = Field(default=None, description="Máximo de entregas a retornar.", ge=1, le=100)


@mcp.tool(
    name="entur_get_webhook_deliveries",
    annotations={
        "title": "Ver histórico de entregas do webhook",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_webhook_deliveries(params: WebhookDeliveriesInput) -> str:
    """Lista o histórico de entregas (sucesso/falha) de um webhook, útil para depurar
    integrações.

    Args:
        params (WebhookDeliveriesInput): id do webhook, limit opcional.

    Returns:
        str: JSON com a lista de entregas do webhook.
    """
    return await run_tool(api_get(f"/webhooks/{params.id}/deliveries", {"limit": params.limit}))
