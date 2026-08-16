"""Ferramentas de Negociações (Deals) do EnturOS CRM.

Uma negociação vive em um funil (pipelineId) com um tipo (pipelineType) e uma etapa
(stageId). O campo status (open/won/lost) é independente da etapa. Marcar "won" ou
"lost" via entur_update_deal roda as automações do funil; ao marcar "lost", informe
lossReasonId (veja entur_list_loss_reasons).
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_delete, api_get, api_patch, api_post
from ..core import mcp
from ..models import DataInput, IdInput, IdWithDataInput
from ..utils import run_tool


class ListDealsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    limit: Optional[int] = Field(default=50, description="Máximo de itens a retornar.", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="Itens a pular, para paginação.", ge=0)
    status: Optional[str] = Field(default=None, description="Filtra por status: 'open', 'won' ou 'lost'.")
    pipeline_id: Optional[str] = Field(default=None, description="Filtra por ID do funil.")
    stage_id: Optional[str] = Field(default=None, description="Filtra por ID da etapa.")
    contact_id: Optional[str] = Field(default=None, description="Filtra pelas negociações de um contato.")


@mcp.tool(
    name="entur_list_deals",
    annotations={
        "title": "Listar negociações",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_deals(params: ListDealsInput) -> str:
    """Lista as negociações (deals) da empresa, com filtros e paginação.

    Args:
        params (ListDealsInput): limit, offset, status ('open'/'won'/'lost'), pipeline_id,
            stage_id, contact_id — todos opcionais.

    Returns:
        str: JSON com "data" (lista de negociações) e "totalCount".
    """
    return await run_tool(
        api_get(
            "/deals",
            {
                "limit": params.limit,
                "offset": params.offset,
                "status": params.status,
                "pipelineId": params.pipeline_id,
                "stageId": params.stage_id,
                "contactId": params.contact_id,
            },
        )
    )


@mcp.tool(
    name="entur_create_deal",
    annotations={
        "title": "Criar negociação",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_deal(params: DataInput) -> str:
    """Cria uma nova negociação (deal) em um funil e etapa.

    Args:
        params (DataInput): data (dict) com os campos da negociação. Campos típicos: title
            (obrigatório), pipelineId (obrigatório, veja entur_list_pipelines), stageId
            (obrigatório, veja entur_get_pipeline_stages), contactId ou accountId,
            valueCents (inteiro, em centavos), ownerId.

    Returns:
        str: JSON da negociação criada.
    """
    return await run_tool(api_post("/deals", params.data))


@mcp.tool(
    name="entur_get_deal",
    annotations={
        "title": "Obter negociação por ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_deal(params: IdInput) -> str:
    """Obtém os dados completos de uma negociação pelo ID.

    Args:
        params (IdInput): id da negociação.

    Returns:
        str: JSON da negociação, ou mensagem de erro se não existir.
    """
    return await run_tool(api_get(f"/deals/{params.id}"))


@mcp.tool(
    name="entur_update_deal",
    annotations={
        "title": "Atualizar negociação (mover etapa, ganhar/perder)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_deal(params: IdWithDataInput) -> str:
    """Atualiza uma negociação: move de etapa, altera valor/dono, ou marca como ganha/perdida.

    IMPORTANTE: definir data={"status": "won"} ou {"status": "lost"} dispara as automações
    do funil (ex: criar automaticamente a venda a partir de um ganho em pré-vendas). Ao
    marcar "lost", inclua também "lossReasonId" (veja entur_list_loss_reasons para os
    motivos válidos do funil). Confirme com o usuário antes de marcar uma negociação como
    ganha ou perdida, pois isso é irreversível via esta ferramenta.

    Args:
        params (IdWithDataInput): id da negociação + data (dict) com os campos a alterar
            (ex: {"stageId": "..."}, {"status": "won"}, {"status": "lost", "lossReasonId": "..."}).

    Returns:
        str: JSON da negociação atualizada.
    """
    return await run_tool(api_patch(f"/deals/{params.id}", params.data))


@mcp.tool(
    name="entur_add_deal_product",
    annotations={
        "title": "Adicionar item (produto) ao negócio",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_add_deal_product(params: IdWithDataInput) -> str:
    """Adiciona um item de catálogo (produto) à negociação, com quantidade e preço.

    Args:
        params (IdWithDataInput): id da negociação + data (dict), tipicamente
            {"productId": "...", "quantity": 1, "unitPriceCents": 100000}.

    Returns:
        str: JSON do item adicionado (deal-product), com seu próprio ID (usado em
            entur_update_deal_product / entur_delete_deal_product).
    """
    return await run_tool(api_post(f"/deals/{params.id}/products", params.data))


class ListLossReasonsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    pipeline_type: Optional[str] = Field(
        default=None,
        description="Filtra por tipo de funil: 'sales', 'pre_sale', 'post_sale', 'support', 'recovery' ou 'custom'.",
    )
    pipeline_id: Optional[str] = Field(default=None, description="Filtra pelos motivos de um funil específico.")


@mcp.tool(
    name="entur_list_loss_reasons",
    annotations={
        "title": "Listar motivos de perda",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_loss_reasons(params: ListLossReasonsInput) -> str:
    """Lista os motivos de perda válidos, opcionalmente filtrados por funil ou tipo de funil.
    Use antes de marcar uma negociação como "lost", para escolher um lossReasonId válido.

    Args:
        params (ListLossReasonsInput): pipeline_type e/ou pipeline_id, opcionais.

    Returns:
        str: JSON com a lista de motivos de perda.
    """
    return await run_tool(
        api_get("/loss-reasons", {"pipelineType": params.pipeline_type, "pipelineId": params.pipeline_id})
    )


class DealTimelineInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(..., description="ID da negociação.", min_length=1)
    categories: Optional[List[str]] = Field(
        default=None, description="Filtra por categorias de evento na timeline (opcional)."
    )
    limit: Optional[int] = Field(default=50, description="Máximo de eventos a retornar.", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="Eventos a pular, para paginação.", ge=0)


@mcp.tool(
    name="entur_get_deal_timeline",
    annotations={
        "title": "Ver linha do tempo da negociação",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_deal_timeline(params: DealTimelineInput) -> str:
    """Retorna a linha do tempo (histórico de eventos) de uma negociação: mudanças de etapa,
    notas, tarefas, mensagens etc.

    Args:
        params (DealTimelineInput): id da negociação, categories (opcional), limit, offset.

    Returns:
        str: JSON com a lista de eventos da timeline, em ordem cronológica.
    """
    return await run_tool(
        api_get(
            f"/deals/{params.id}/timeline",
            {"categories": params.categories, "limit": params.limit, "offset": params.offset},
        )
    )


@mcp.tool(
    name="entur_get_deal_playbook",
    annotations={
        "title": "Ver playbook resolvido da negociação",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_deal_playbook(params: IdInput) -> str:
    """Retorna o playbook (guia de vendas por etapa) já resolvido para a etapa atual da
    negociação: o que fazer, quais ações estão pendentes.

    Args:
        params (IdInput): id da negociação.

    Returns:
        str: JSON com o playbook resolvido para a negociação.
    """
    return await run_tool(api_get(f"/deals/{params.id}/playbook"))


@mcp.tool(
    name="entur_get_deal_ai_insights",
    annotations={
        "title": "Ver inteligência de IA da negociação",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_deal_ai_insights(params: IdInput) -> str:
    """Retorna as análises de IA já geradas pelo CRM para esta negociação (ex: risco de
    perda, próximas ações sugeridas, resumo).

    Args:
        params (IdInput): id da negociação.

    Returns:
        str: JSON com os insights de IA da negociação.
    """
    return await run_tool(api_get(f"/deals/{params.id}/ai"))


@mcp.tool(
    name="entur_update_deal_product",
    annotations={
        "title": "Editar item do negócio",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_deal_product(params: IdWithDataInput) -> str:
    """Edita um item (produto) já adicionado a uma negociação (ex: quantidade ou preço).

    Args:
        params (IdWithDataInput): id do item do negócio (deal-product, não o id da
            negociação) + data (dict) com os campos a alterar.

    Returns:
        str: JSON do item atualizado.
    """
    return await run_tool(api_patch(f"/deal-products/{params.id}", params.data))


@mcp.tool(
    name="entur_delete_deal_product",
    annotations={
        "title": "Remover item do negócio",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_delete_deal_product(params: IdInput) -> str:
    """Remove um item (produto) de uma negociação.

    Args:
        params (IdInput): id do item do negócio (deal-product) a remover.

    Returns:
        str: JSON de confirmação, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/deal-products/{params.id}"))
