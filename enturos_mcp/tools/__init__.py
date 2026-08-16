"""Importa todos os módulos de ferramentas para que se registrem em `enturos_mcp.core.mcp`."""

from . import (
    accounts,
    analytics,
    catalogs,
    contacts,
    custom_fields,
    deals,
    notes,
    oauth,
    pipelines,
    products,
    proposals,
    rfv,
    segments,
    tags,
    tasks,
    webhooks,
)

__all__ = [
    "accounts",
    "analytics",
    "catalogs",
    "contacts",
    "custom_fields",
    "deals",
    "notes",
    "oauth",
    "pipelines",
    "products",
    "proposals",
    "rfv",
    "segments",
    "tags",
    "tasks",
    "webhooks",
]
