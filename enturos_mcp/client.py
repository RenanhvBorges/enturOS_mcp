"""Cliente HTTP para a API REST do EnturOS CRM (https://crm.enturos.com/api/v1/docs)."""

from typing import Any, Dict, Optional

import httpx

from . import config


class EnturOSAPIError(Exception):
    """Erro ao chamar a API do EnturOS CRM, com mensagem já pronta para o usuário final."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


def _require_api_key() -> str:
    if not config.API_KEY:
        raise EnturOSAPIError(
            "ENTUROS_API_KEY não está configurada. Defina a variável de ambiente "
            "ENTUROS_API_KEY com a chave da API do EnturOS CRM (gerada no painel, "
            "formato enturos_live_... ou enturos_test_...) e reinicie o servidor MCP."
        )
    return config.API_KEY


def _extract_error_detail(response: httpx.Response) -> str:
    try:
        body = response.json()
        return body.get("detail") or body.get("title") or response.text[:500]
    except ValueError:
        return response.text[:500] or f"status {response.status_code}"


async def api_request(
    method: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    json_body: Optional[Dict[str, Any]] = None,
) -> Any:
    """Executa uma chamada autenticada à API do EnturOS CRM e retorna o corpo JSON já decodificado."""
    api_key = _require_api_key()

    clean_params = {k: v for k, v in (params or {}).items() if v is not None}

    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient(
        base_url=config.API_BASE_URL, timeout=config.REQUEST_TIMEOUT_SECONDS
    ) as client:
        try:
            response = await client.request(
                method,
                path,
                params=clean_params or None,
                json=json_body,
                headers=headers,
            )
        except httpx.TimeoutException as e:
            raise EnturOSAPIError(
                "Tempo limite excedido ao chamar a API do EnturOS CRM. Tente novamente em instantes."
            ) from e
        except httpx.RequestError as e:
            raise EnturOSAPIError(
                f"Erro de rede ao chamar a API do EnturOS CRM em {config.API_BASE_URL}: {e}. "
                "Se o erro mencionar DNS/nome do servidor, confira se ENTUROS_API_BASE_URL "
                "está correto (verifique com o suporte do EnturOS qual é o endereço atual da API)."
            ) from e

    if response.status_code == 401:
        raise EnturOSAPIError(
            "Credencial inválida, expirada ou revogada (401). Verifique a variável "
            "ENTUROS_API_KEY.",
            401,
        )
    if response.status_code == 403:
        raise EnturOSAPIError(
            f"Permissão negada (403): {_extract_error_detail(response)}. A credencial "
            "não tem o escopo necessário para esta operação.",
            403,
        )
    if response.status_code == 404:
        raise EnturOSAPIError(
            f"Não encontrado (404): {_extract_error_detail(response)}",
            404,
        )
    if response.status_code == 422:
        raise EnturOSAPIError(
            f"Dados inválidos (422): {_extract_error_detail(response)}",
            422,
        )
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", "alguns segundos")
        raise EnturOSAPIError(
            f"Limite de requisições atingido (429). Aguarde {retry_after}s e tente novamente.",
            429,
        )
    if response.status_code >= 400:
        raise EnturOSAPIError(
            f"Erro {response.status_code} da API do EnturOS CRM: "
            f"{_extract_error_detail(response)}",
            response.status_code,
        )

    if response.status_code == 204 or not response.content:
        return {}
    return response.json()


async def api_get(path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    return await api_request("GET", path, params=params)


async def api_post(path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
    return await api_request("POST", path, json_body=json_body)


async def api_patch(path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
    return await api_request("PATCH", path, json_body=json_body)


async def api_put(path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
    return await api_request("PUT", path, json_body=json_body)


async def api_delete(path: str, json_body: Optional[Dict[str, Any]] = None) -> Any:
    return await api_request("DELETE", path, json_body=json_body)
