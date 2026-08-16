"""Ferramentas de Analytics / KPIs do EnturOS CRM.

Leitura: resumo do funil, receita por período, motivos de perda, funil por etapa e
conversão. Agregações da própria empresa; aceitam filtros de período, funil, dono,
origem, UTM.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_get
from ..core import mcp
from ..utils import run_tool


class DateRangeInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    date_from: Optional[str] = Field(default=None, description="Data inicial (ISO 8601, ex: '2026-01-01').")
    date_to: Optional[str] = Field(default=None, description="Data final (ISO 8601, ex: '2026-01-31').")
    pipeline_id: Optional[str] = Field(default=None, description="Filtra por ID do funil.")


class AnalyticsSummaryInput(DateRangeInput):
    pipeline_type: Optional[str] = Field(
        default=None,
        description="Filtra por tipo de funil: 'sales', 'pre_sale', 'post_sale', 'support', 'recovery' ou 'custom'.",
    )


@mcp.tool(
    name="entur_get_analytics_summary",
    annotations={
        "title": "Resumo de KPIs do funil",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_analytics_summary(params: AnalyticsSummaryInput) -> str:
    """Retorna o resumo de KPIs do funil de vendas (ex: total de negociações, receita,
    taxa de conversão), agregado no período e filtros informados.

    Args:
        params (AnalyticsSummaryInput): date_from, date_to, pipeline_id, pipeline_type,
            todos opcionais.

    Returns:
        str: JSON com o resumo de KPIs.
    """
    return await run_tool(
        api_get(
            "/analytics/summary",
            {
                "dateFrom": params.date_from,
                "dateTo": params.date_to,
                "pipelineId": params.pipeline_id,
                "pipelineType": params.pipeline_type,
            },
        )
    )


class AnalyticsLossReasonsInput(DateRangeInput):
    limit: Optional[int] = Field(default=10, description="Máximo de motivos a retornar.", ge=1, le=100)


@mcp.tool(
    name="entur_get_analytics_loss_reasons",
    annotations={
        "title": "Top motivos de perda",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_analytics_loss_reasons(params: AnalyticsLossReasonsInput) -> str:
    """Retorna o ranking dos motivos de perda mais frequentes, no período e filtros informados.

    Args:
        params (AnalyticsLossReasonsInput): limit, date_from, date_to, pipeline_id.

    Returns:
        str: JSON com o ranking de motivos de perda.
    """
    return await run_tool(
        api_get(
            "/analytics/loss-reasons",
            {
                "limit": params.limit,
                "dateFrom": params.date_from,
                "dateTo": params.date_to,
                "pipelineId": params.pipeline_id,
            },
        )
    )


@mcp.tool(
    name="entur_get_analytics_deals_by_period",
    annotations={
        "title": "Negócios por período (série temporal)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_analytics_deals_by_period(params: DateRangeInput) -> str:
    """Retorna a série temporal de negociações criadas/fechadas por período.

    Args:
        params (DateRangeInput): date_from, date_to, pipeline_id, todos opcionais.

    Returns:
        str: JSON com a série temporal de negociações.
    """
    return await run_tool(
        api_get(
            "/analytics/deals-by-period",
            {"dateFrom": params.date_from, "dateTo": params.date_to, "pipelineId": params.pipeline_id},
        )
    )


class FunnelInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    pipeline_id: str = Field(..., description="ID do funil (obrigatório).", min_length=1)
    date_from: Optional[str] = Field(default=None, description="Data inicial (ISO 8601).")
    date_to: Optional[str] = Field(default=None, description="Data final (ISO 8601).")


@mcp.tool(
    name="entur_get_analytics_funnel",
    annotations={
        "title": "Funil por etapa (contagem + valor)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_analytics_funnel(params: FunnelInput) -> str:
    """Retorna, para um funil específico, a contagem de negociações e o valor total em
    cada etapa.

    Args:
        params (FunnelInput): pipeline_id (obrigatório), date_from, date_to (opcionais).

    Returns:
        str: JSON com contagem e valor por etapa do funil.
    """
    return await run_tool(
        api_get(
            "/analytics/funnel",
            {"pipelineId": params.pipeline_id, "dateFrom": params.date_from, "dateTo": params.date_to},
        )
    )


@mcp.tool(
    name="entur_get_analytics_funnel_conversion",
    annotations={
        "title": "Conversão etapa a etapa",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_analytics_funnel_conversion(params: FunnelInput) -> str:
    """Retorna a taxa de conversão entre cada etapa consecutiva de um funil.

    Args:
        params (FunnelInput): pipeline_id (obrigatório), date_from, date_to (opcionais).

    Returns:
        str: JSON com a taxa de conversão etapa a etapa.
    """
    return await run_tool(
        api_get(
            "/analytics/funnel-conversion",
            {"pipelineId": params.pipeline_id, "dateFrom": params.date_from, "dateTo": params.date_to},
        )
    )
