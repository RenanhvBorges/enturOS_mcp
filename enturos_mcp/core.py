"""Instância central do servidor MCP, compartilhada por todos os módulos de ferramentas."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("enturos_mcp")
