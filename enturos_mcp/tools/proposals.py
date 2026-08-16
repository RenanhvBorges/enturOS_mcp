"""Ferramentas de Propostas comerciais do EnturOS CRM.

Uma proposta nasce de um negócio com produtos; o design é a página pública em /p/{token}
(retornada como publicUrl). Monte os dados + tema e compartilhe o link.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_get, api_patch, api_post
from ..core import mcp
from ..models import DataInput, IdInput, IdWithDataInput
from ..utils import run_tool


class ListProposalsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    deal_id: Optional[str] = Field(default=None, description="Filtra pelas propostas de uma negociação.")
    status: Optional[str] = Field(default=None, description="Filtra por status da proposta.")


@mcp.tool(
    name="entur_list_proposals",
    annotations={
        "title": "Listar propostas",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_proposals(params: ListProposalsInput) -> str:
    """Lista propostas comerciais, opcionalmente filtradas por negociação ou status.

    Args:
        params (ListProposalsInput): deal_id e/ou status, opcionais.

    Returns:
        str: JSON com a lista de propostas.
    """
    return await run_tool(api_get("/proposals", {"dealId": params.deal_id, "status": params.status}))


@mcp.tool(
    name="entur_create_proposal",
    annotations={
        "title": "Criar proposta a partir de um negócio",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_proposal(params: DataInput) -> str:
    """Cria uma nova proposta comercial a partir de uma negociação (deal) já com produtos.

    Args:
        params (DataInput): data (dict) com os campos da proposta. Campo típico: dealId
            (obrigatório, a negociação de origem). Os itens da proposta normalmente vêm
            dos produtos já adicionados ao negócio (veja entur_add_deal_product).

    Returns:
        str: JSON da proposta criada.
    """
    return await run_tool(api_post("/proposals", params.data))


@mcp.tool(
    name="entur_get_proposal",
    annotations={
        "title": "Obter proposta por ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_proposal(params: IdInput) -> str:
    """Obtém os dados completos de uma proposta pelo ID.

    Args:
        params (IdInput): id da proposta.

    Returns:
        str: JSON da proposta, ou mensagem de erro se não existir.
    """
    return await run_tool(api_get(f"/proposals/{params.id}"))


@mcp.tool(
    name="entur_update_proposal",
    annotations={
        "title": "Atualizar proposta (tema + viagem)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_proposal(params: IdWithDataInput) -> str:
    """Atualiza os dados de tema visual e/ou informações da viagem de uma proposta.

    Args:
        params (IdWithDataInput): id da proposta + data (dict) com os campos a alterar
            (ex: tema de cores, título da viagem, datas).

    Returns:
        str: JSON da proposta atualizada.
    """
    return await run_tool(api_patch(f"/proposals/{params.id}", params.data))


@mcp.tool(
    name="entur_get_proposal_items",
    annotations={
        "title": "Ver itens da proposta",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_proposal_items(params: IdInput) -> str:
    """Lista os itens (produtos/serviços) incluídos em uma proposta.

    Args:
        params (IdInput): id da proposta.

    Returns:
        str: JSON com a lista de itens da proposta.
    """
    return await run_tool(api_get(f"/proposals/{params.id}/items"))


@mcp.tool(
    name="entur_get_proposal_public_link",
    annotations={
        "title": "Obter link público da proposta",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_proposal_public_link(params: IdInput) -> str:
    """Obtém o link público (publicUrl, no formato /p/{token}) para compartilhar a proposta
    com o cliente.

    Args:
        params (IdInput): id da proposta.

    Returns:
        str: JSON contendo publicUrl.
    """
    return await run_tool(api_get(f"/proposals/{params.id}/public-link"))


@mcp.tool(
    name="entur_send_proposal",
    annotations={
        "title": "Marcar proposta como enviada",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_send_proposal(params: IdInput) -> str:
    """Marca a proposta como enviada ao cliente (não envia email, apenas registra o status).

    Args:
        params (IdInput): id da proposta.

    Returns:
        str: JSON da proposta atualizada.
    """
    return await run_tool(api_post(f"/proposals/{params.id}/send"))


@mcp.tool(
    name="entur_get_proposal_itinerary",
    annotations={
        "title": "Ver roteiro da proposta",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_proposal_itinerary(params: IdInput) -> str:
    """Retorna o roteiro dia-a-dia (itinerary) de uma proposta de viagem.

    Args:
        params (IdInput): id da proposta.

    Returns:
        str: JSON com a lista de dias do roteiro.
    """
    return await run_tool(api_get(f"/proposals/{params.id}/itinerary"))


@mcp.tool(
    name="entur_add_proposal_itinerary_day",
    annotations={
        "title": "Adicionar/editar dia do roteiro",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_add_proposal_itinerary_day(params: IdWithDataInput) -> str:
    """Adiciona ou edita um dia do roteiro da proposta, podendo incluir fotos.

    Args:
        params (IdWithDataInput): id da proposta + data (dict) com o dia do roteiro
            (ex: {"day": 1, "title": "...", "description": "...", "photoUrls": [...]}).

    Returns:
        str: JSON do dia do roteiro salvo.
    """
    return await run_tool(api_post(f"/proposals/{params.id}/itinerary", params.data))


@mcp.tool(
    name="entur_get_proposal_flights",
    annotations={
        "title": "Ver voos da proposta",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_proposal_flights(params: IdInput) -> str:
    """Lista os voos incluídos em uma proposta.

    Args:
        params (IdInput): id da proposta.

    Returns:
        str: JSON com a lista de voos.
    """
    return await run_tool(api_get(f"/proposals/{params.id}/flights"))


@mcp.tool(
    name="entur_add_proposal_flight",
    annotations={
        "title": "Adicionar voo à proposta",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_add_proposal_flight(params: IdWithDataInput) -> str:
    """Adiciona um voo (cartão de embarque) à proposta.

    Args:
        params (IdWithDataInput): id da proposta + data (dict) com os dados do voo
            (ex: companhia aérea, número do voo, origem, destino, datas/horários).

    Returns:
        str: JSON do voo adicionado.
    """
    return await run_tool(api_post(f"/proposals/{params.id}/flights", params.data))


@mcp.tool(
    name="entur_get_proposal_hotels",
    annotations={
        "title": "Ver hotéis da proposta",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_proposal_hotels(params: IdInput) -> str:
    """Lista os hotéis incluídos em uma proposta.

    Args:
        params (IdInput): id da proposta.

    Returns:
        str: JSON com a lista de hotéis.
    """
    return await run_tool(api_get(f"/proposals/{params.id}/hotels"))


@mcp.tool(
    name="entur_add_proposal_hotel",
    annotations={
        "title": "Adicionar hotel à proposta",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_add_proposal_hotel(params: IdWithDataInput) -> str:
    """Adiciona um hotel (com imagens) à proposta.

    Args:
        params (IdWithDataInput): id da proposta + data (dict) com os dados do hotel
            (ex: nome, endereço, datas de check-in/check-out, imageUrls).

    Returns:
        str: JSON do hotel adicionado.
    """
    return await run_tool(api_post(f"/proposals/{params.id}/hotels", params.data))
