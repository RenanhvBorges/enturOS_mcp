"""Ferramentas de Contas (empresas B2B) do EnturOS CRM.

Um contato pode ser o primaryContactId de uma conta.
"""

from ..client import api_get, api_patch, api_post
from ..core import mcp
from ..models import DataInput, IdInput, IdWithDataInput, SearchInput
from ..utils import run_tool


@mcp.tool(
    name="entur_list_accounts",
    annotations={
        "title": "Listar contas (B2B)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_accounts(params: SearchInput) -> str:
    """Lista as contas (empresas B2B) da empresa, com busca textual e paginação.

    Args:
        params (SearchInput): search (nome/domínio), limit, offset.

    Returns:
        str: JSON com "data" (lista de contas) e "totalCount".
    """
    return await run_tool(
        api_get("/accounts", {"limit": params.limit, "offset": params.offset, "search": params.search})
    )


@mcp.tool(
    name="entur_create_account",
    annotations={
        "title": "Criar conta (B2B)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_account(params: DataInput) -> str:
    """Cria uma nova conta (empresa B2B).

    Args:
        params (DataInput): data (dict) com os campos da conta. Campos típicos: name
            (obrigatório), domain, primaryContactId (ID de um contato existente),
            segmentId (veja entur_list_account_segments).

    Returns:
        str: JSON da conta criada.
    """
    return await run_tool(api_post("/accounts", params.data))


@mcp.tool(
    name="entur_get_account",
    annotations={
        "title": "Obter conta por ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_account(params: IdInput) -> str:
    """Obtém os dados completos de uma conta (B2B) pelo ID.

    Args:
        params (IdInput): id da conta.

    Returns:
        str: JSON da conta, ou mensagem de erro se não existir.
    """
    return await run_tool(api_get(f"/accounts/{params.id}"))


@mcp.tool(
    name="entur_update_account",
    annotations={
        "title": "Atualizar conta (B2B)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_account(params: IdWithDataInput) -> str:
    """Atualiza campos de uma conta (B2B) existente (atualização parcial).

    Args:
        params (IdWithDataInput): id da conta + data (dict) com os campos a alterar.

    Returns:
        str: JSON da conta atualizada.
    """
    return await run_tool(api_patch(f"/accounts/{params.id}", params.data))
