"""Configuração do servidor, lida a partir de variáveis de ambiente."""

import os

DEFAULT_API_BASE_URL = "https://crm.enturos.com/api/v1"

API_BASE_URL = os.environ.get("ENTUROS_API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")
API_KEY = os.environ.get("ENTUROS_API_KEY", "").strip()
REQUEST_TIMEOUT_SECONDS = float(os.environ.get("ENTUROS_TIMEOUT_SECONDS", "30"))
