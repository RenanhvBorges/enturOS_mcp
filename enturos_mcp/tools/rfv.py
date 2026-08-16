"""Ferramentas de RFV / lead scoring (Recência-Frequência-Valor) do EnturOS CRM."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_get
from ..core import mcp
from ..utils import run_tool


class RfvDashboardInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    audience_type: Optional[str] = Field(default=None, description="Filtra por tipo de audiência.")
    smart_filter: Optional[str] = Field(default=None, description="Filtro inteligente pré-definido do RFV.")


@mcp.tool(
    name="entur_get_rfv_dashboard",
    annotations={
        "title": "RFV — distribuição (dashboard)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_rfv_dashboard(params: RfvDashboardInput) -> str:
    """Retorna a distribuição de contatos por score RFV (Recência-Frequência-Valor), para
    montar um dashboard de lead scoring.

    Args:
        params (RfvDashboardInput): audience_type, smart_filter, ambos opcionais.

    Returns:
        str: JSON com a distribuição RFV.
    """
    return await run_tool(
        api_get("/rfv/dashboard", {"audienceType": params.audience_type, "smartFilter": params.smart_filter})
    )


class RfvContactsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    search: Optional[str] = Field(default=None, description="Texto livre para buscar (nome/email).")
    audience_type: Optional[str] = Field(default=None, description="Filtra por tipo de audiência.")
    smart_filter: Optional[str] = Field(default=None, description="Filtro inteligente pré-definido do RFV.")
    limit: Optional[int] = Field(default=50, description="Máximo de itens a retornar.", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="Itens a pular, para paginação.", ge=0)


@mcp.tool(
    name="entur_list_rfv_contacts",
    annotations={
        "title": "RFV — contatos com score",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_rfv_contacts(params: RfvContactsInput) -> str:
    """Lista contatos com seu score de RFV (Recência-Frequência-Valor), com busca e filtros.

    Args:
        params (RfvContactsInput): search, audience_type, smart_filter, limit, offset.

    Returns:
        str: JSON com "data" (contatos + score) e "totalCount".
    """
    return await run_tool(
        api_get(
            "/rfv/contacts",
            {
                "search": params.search,
                "audienceType": params.audience_type,
                "smartFilter": params.smart_filter,
                "limit": params.limit,
                "offset": params.offset,
            },
        )
    )
