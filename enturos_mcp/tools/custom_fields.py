"""Ferramentas de Campos personalizados do EnturOS CRM.

Campos personalizados têm duas camadas: a DEFINIÇÃO (schema do campo, em /custom-fields,
exige custom_fields:write) e o VALOR preenchido num registro (em
/{contacts|deals|accounts}/{id}/custom-fields, exige o escopo de escrita da entidade).
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_delete, api_get, api_patch, api_post, api_put
from ..core import mcp
from ..models import DataInput, IdInput, IdWithDataInput
from ..utils import run_tool


class ListCustomFieldDefinitionsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    entity: str = Field(
        ..., description="Entidade dona do campo: 'contacts', 'deals' ou 'accounts' (obrigatório).", min_length=1
    )
    pipeline_id: Optional[str] = Field(
        default=None, description="Filtra campos específicos de um funil (quando aplicável)."
    )


@mcp.tool(
    name="entur_list_custom_field_definitions",
    annotations={
        "title": "Listar definições de campos personalizados",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_custom_field_definitions(params: ListCustomFieldDefinitionsInput) -> str:
    """Lista as definições (schema) de campos personalizados de uma entidade.

    Args:
        params (ListCustomFieldDefinitionsInput): entity ('contacts'/'deals'/'accounts',
            obrigatório), pipeline_id (opcional).

    Returns:
        str: JSON com a lista de definições de campos.
    """
    return await run_tool(
        api_get("/custom-fields", {"entity": params.entity, "pipelineId": params.pipeline_id})
    )


@mcp.tool(
    name="entur_create_custom_field_definition",
    annotations={
        "title": "Criar definição de campo personalizado",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_custom_field_definition(params: DataInput) -> str:
    """Cria uma nova definição (schema) de campo personalizado para uma entidade. Isso
    altera o schema da empresa inteira — use com cautela e confirme com o usuário.

    Args:
        params (DataInput): data (dict) com os campos da definição. Campos típicos: entity
            ('contacts'/'deals'/'accounts', obrigatório), name (obrigatório), type
            (ex: 'text', 'number', 'date', 'select'), options (lista, se type='select').

    Returns:
        str: JSON da definição de campo criada.
    """
    return await run_tool(api_post("/custom-fields", params.data))


@mcp.tool(
    name="entur_update_custom_field_definition",
    annotations={
        "title": "Editar definição de campo personalizado",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_custom_field_definition(params: IdWithDataInput) -> str:
    """Edita a definição (schema) de um campo personalizado já existente.

    Args:
        params (IdWithDataInput): id da definição de campo + data (dict) com os campos a alterar.

    Returns:
        str: JSON da definição de campo atualizada.
    """
    return await run_tool(api_patch(f"/custom-fields/{params.id}", params.data))


@mcp.tool(
    name="entur_archive_custom_field_definition",
    annotations={
        "title": "Arquivar definição de campo personalizado",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_archive_custom_field_definition(params: IdInput) -> str:
    """Arquiva (soft-delete reversível) uma definição de campo personalizado. Pode ser
    restaurada com entur_restore_custom_field_definition.

    Args:
        params (IdInput): id da definição de campo a arquivar.

    Returns:
        str: JSON de confirmação, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/custom-fields/{params.id}"))


@mcp.tool(
    name="entur_restore_custom_field_definition",
    annotations={
        "title": "Restaurar definição de campo personalizado",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_restore_custom_field_definition(params: IdInput) -> str:
    """Restaura uma definição de campo personalizado previamente arquivada.

    Args:
        params (IdInput): id da definição de campo a restaurar.

    Returns:
        str: JSON da definição de campo restaurada.
    """
    return await run_tool(api_post(f"/custom-fields/{params.id}/restore"))


@mcp.tool(
    name="entur_get_contact_custom_fields",
    annotations={
        "title": "Ler valores de campos personalizados do contato",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_contact_custom_fields(params: IdInput) -> str:
    """Lê os valores de campos personalizados preenchidos num contato.

    Args:
        params (IdInput): id do contato.

    Returns:
        str: JSON com os valores dos campos personalizados do contato.
    """
    return await run_tool(api_get(f"/contacts/{params.id}/custom-fields"))


@mcp.tool(
    name="entur_set_contact_custom_fields",
    annotations={
        "title": "Gravar valores de campos personalizados do contato",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_set_contact_custom_fields(params: IdWithDataInput) -> str:
    """Grava (upsert) os valores de campos personalizados de um contato.

    Args:
        params (IdWithDataInput): id do contato + data (dict mapeando o nome/ID de cada
            campo personalizado ao valor a gravar).

    Returns:
        str: JSON com os valores salvos.
    """
    return await run_tool(api_put(f"/contacts/{params.id}/custom-fields", params.data))


@mcp.tool(
    name="entur_get_deal_custom_fields",
    annotations={
        "title": "Ler valores de campos personalizados da negociação",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_deal_custom_fields(params: IdInput) -> str:
    """Lê os valores de campos personalizados preenchidos numa negociação.

    Args:
        params (IdInput): id da negociação.

    Returns:
        str: JSON com os valores dos campos personalizados da negociação.
    """
    return await run_tool(api_get(f"/deals/{params.id}/custom-fields"))


@mcp.tool(
    name="entur_set_deal_custom_fields",
    annotations={
        "title": "Gravar valores de campos personalizados da negociação",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_set_deal_custom_fields(params: IdWithDataInput) -> str:
    """Grava (upsert) os valores de campos personalizados de uma negociação.

    Args:
        params (IdWithDataInput): id da negociação + data (dict mapeando o nome/ID de cada
            campo personalizado ao valor a gravar).

    Returns:
        str: JSON com os valores salvos.
    """
    return await run_tool(api_put(f"/deals/{params.id}/custom-fields", params.data))


@mcp.tool(
    name="entur_get_account_custom_fields",
    annotations={
        "title": "Ler valores de campos personalizados da conta",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_account_custom_fields(params: IdInput) -> str:
    """Lê os valores de campos personalizados preenchidos numa conta (B2B).

    Args:
        params (IdInput): id da conta.

    Returns:
        str: JSON com os valores dos campos personalizados da conta.
    """
    return await run_tool(api_get(f"/accounts/{params.id}/custom-fields"))


@mcp.tool(
    name="entur_set_account_custom_fields",
    annotations={
        "title": "Gravar valores de campos personalizados da conta",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_set_account_custom_fields(params: IdWithDataInput) -> str:
    """Grava (upsert) os valores de campos personalizados de uma conta (B2B).

    Args:
        params (IdWithDataInput): id da conta + data (dict mapeando o nome/ID de cada
            campo personalizado ao valor a gravar).

    Returns:
        str: JSON com os valores salvos.
    """
    return await run_tool(api_put(f"/accounts/{params.id}/custom-fields", params.data))
