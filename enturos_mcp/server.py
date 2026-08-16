"""Ponto de entrada do servidor MCP do EnturOS CRM (transporte stdio)."""

from .core import mcp
from . import tools  # noqa: F401  - importar registra todas as ferramentas em `mcp`


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
