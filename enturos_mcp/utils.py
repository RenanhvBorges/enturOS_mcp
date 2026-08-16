"""Utilitários compartilhados pelas ferramentas: formatação de resposta e tratamento de erro."""

import json
from typing import Any, Awaitable

from .client import EnturOSAPIError


def _default_json(value: Any) -> str:
    return str(value)


async def run_tool(coro: Awaitable[Any]) -> str:
    """Executa a chamada à API e devolve JSON formatado, ou uma mensagem de erro acionável."""
    try:
        result = await coro
    except EnturOSAPIError as e:
        return f"Erro: {e}"
    except Exception as e:  # noqa: BLE001 - queremos nunca quebrar a ferramenta MCP
        return f"Erro inesperado ({type(e).__name__}): {e}"
    return json.dumps(result, indent=2, ensure_ascii=False, default=_default_json)
