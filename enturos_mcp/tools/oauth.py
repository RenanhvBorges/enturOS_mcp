"""Ferramenta para o fluxo OAuth2 client_credentials do EnturOS CRM.

Uso avançado: a maioria dos usuários deste servidor MCP já se autentica via API key
(ENTUROS_API_KEY) e não precisa desta ferramenta. Ela existe para quem gerencia
integrações OAuth2 próprias (client_id/client_secret) separadas da API key deste servidor.
"""

from typing import List, Optional

import json

import httpx
from pydantic import BaseModel, ConfigDict, Field

from .. import config
from ..core import mcp


class IssueOAuthTokenInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    client_id: str = Field(..., description="Client ID OAuth2 do EnturOS CRM.", min_length=1)
    client_secret: str = Field(..., description="Client secret OAuth2 do EnturOS CRM.", min_length=1)
    scope: Optional[List[str]] = Field(
        default=None, description="Lista de escopos solicitados (ex: ['contacts:read', 'deals:read'])."
    )


async def _issue_token(client_id: str, client_secret: str, scope: Optional[str]) -> dict:
    data = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}
    if scope:
        data["scope"] = scope
    async with httpx.AsyncClient(
        base_url=config.API_BASE_URL, timeout=config.REQUEST_TIMEOUT_SECONDS
    ) as client:
        response = await client.post("/oauth/token", data=data)
        response.raise_for_status()
        return response.json()


@mcp.tool(
    name="entur_issue_oauth_token",
    annotations={
        "title": "Emitir access token OAuth2 (client_credentials)",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_issue_oauth_token(params: IssueOAuthTokenInput) -> str:
    """Troca um client_id/client_secret OAuth2 por um access_token de curta duração
    (válido por 1 hora). Uso avançado — a maioria das integrações deve usar a API key
    (ENTUROS_API_KEY) configurada neste servidor, não esta ferramenta.

    Args:
        params (IssueOAuthTokenInput): client_id, client_secret, scope (lista opcional).

    Returns:
        str: JSON com access_token, token_type e expires_in.
    """
    try:
        scope_str = " ".join(params.scope) if params.scope else None
        result = await _issue_token(params.client_id, params.client_secret, scope_str)
    except httpx.HTTPStatusError as e:
        return f"Erro: falha ao emitir token OAuth2 (status {e.response.status_code}): {e.response.text[:300]}"
    except httpx.HTTPError as e:
        return f"Erro: falha de rede ao emitir token OAuth2: {e}"
    return json.dumps(result, indent=2, ensure_ascii=False)
