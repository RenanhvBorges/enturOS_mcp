"""Ferramentas do Catálogo de produtos do EnturOS CRM."""

from ..client import api_get
from ..core import mcp
from ..models import IdInput, SearchInput
from ..utils import run_tool


@mcp.tool(
    name="entur_list_products",
    annotations={
        "title": "Listar produtos do catálogo",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_products(params: SearchInput) -> str:
    """Lista os produtos do catálogo da empresa, com busca textual e paginação.

    Args:
        params (SearchInput): search (nome do produto), limit, offset.

    Returns:
        str: JSON com "data" (lista de produtos) e "totalCount".
    """
    return await run_tool(
        api_get("/products", {"limit": params.limit, "offset": params.offset, "search": params.search})
    )


@mcp.tool(
    name="entur_get_product",
    annotations={
        "title": "Obter produto por ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_product(params: IdInput) -> str:
    """Obtém os dados completos de um produto do catálogo pelo ID.

    Args:
        params (IdInput): id do produto.

    Returns:
        str: JSON do produto, ou mensagem de erro se não existir.
    """
    return await run_tool(api_get(f"/products/{params.id}"))


@mcp.tool(
    name="entur_get_deal_products",
    annotations={
        "title": "Ver produtos de uma negociação",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_deal_products(params: IdInput) -> str:
    """Lista os itens (produtos) já adicionados a uma negociação.

    Args:
        params (IdInput): id da negociação (deal).

    Returns:
        str: JSON com a lista de itens do negócio.
    """
    return await run_tool(api_get(f"/deals/{params.id}/products"))
