"""Ferramentas de Contatos e Fidelidade do EnturOS CRM.

Cobre: /contacts, /contacts/duplicates, /contacts/merge, /contacts/{id}/attribution,
/contacts/{id}/travel-preferences, /contacts/{id}/referral-credit, /contacts/{id}/loyalty,
/loyalty-programs/{id}.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_delete, api_get, api_patch, api_post, api_put
from ..core import mcp
from ..models import DataInput, IdInput, IdWithDataInput, SearchInput
from ..utils import run_tool


@mcp.tool(
    name="entur_list_contacts",
    annotations={
        "title": "Listar contatos",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_contacts(params: SearchInput) -> str:
    """Lista os contatos da empresa, com busca textual e paginação.

    Args:
        params (SearchInput): search (nome/email/telefone), limit (padrão 50, máx 100), offset.

    Returns:
        str: JSON com "data" (lista de contatos) e "totalCount".
    """
    return await run_tool(
        api_get(
            "/contacts",
            {"limit": params.limit, "offset": params.offset, "search": params.search},
        )
    )


@mcp.tool(
    name="entur_create_contact",
    annotations={
        "title": "Criar contato",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_contact(params: DataInput) -> str:
    """Cria um novo contato.

    Args:
        params (DataInput): data (dict) com os campos do contato. Campos típicos: name (obrigatório),
            email, phone, ownerId, source, utm (dict), tags (lista de nomes). Use entur_list_contacts
            ou entur_find_duplicate_contacts antes de criar, para evitar duplicidade.

    Returns:
        str: JSON do contato criado.
    """
    return await run_tool(api_post("/contacts", params.data))


@mcp.tool(
    name="entur_get_contact",
    annotations={
        "title": "Obter contato por ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_contact(params: IdInput) -> str:
    """Obtém os dados completos de um contato pelo ID.

    Args:
        params (IdInput): id do contato.

    Returns:
        str: JSON do contato, ou "Erro: ... 404 ..." se não existir para esta empresa.
    """
    return await run_tool(api_get(f"/contacts/{params.id}"))


@mcp.tool(
    name="entur_update_contact",
    annotations={
        "title": "Atualizar contato",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_contact(params: IdWithDataInput) -> str:
    """Atualiza campos de um contato existente (atualização parcial).

    Args:
        params (IdWithDataInput): id do contato + data (dict) com os campos a alterar
            (ex: {"name": "...", "email": "...", "phone": "...", "ownerId": "..."}).

    Returns:
        str: JSON do contato atualizado.
    """
    return await run_tool(api_patch(f"/contacts/{params.id}", params.data))


@mcp.tool(
    name="entur_delete_contact",
    annotations={
        "title": "Excluir contato",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_delete_contact(params: IdInput) -> str:
    """Exclui um contato definitivamente. AÇÃO DESTRUTIVA: confirme explicitamente com o
    usuário antes de chamar esta ferramenta, informando qual contato será excluído.

    Args:
        params (IdInput): id do contato a excluir.

    Returns:
        str: JSON de confirmação, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/contacts/{params.id}"))


class FindDuplicateContactsInput(BaseModel):
    """Filtros para localizar contatos potencialmente duplicados."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    email: Optional[str] = Field(default=None, description="Email para checar duplicidade.")
    phone: Optional[str] = Field(default=None, description="Telefone para checar duplicidade.")
    name: Optional[str] = Field(default=None, description="Nome para checar duplicidade.")
    exclude_contact_id: Optional[str] = Field(
        default=None, description="ID de contato a excluir da checagem (ex: o próprio contato sendo editado)."
    )


@mcp.tool(
    name="entur_find_duplicate_contacts",
    annotations={
        "title": "Achar contatos duplicados",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_find_duplicate_contacts(params: FindDuplicateContactsInput) -> str:
    """Busca contatos potencialmente duplicados por email, telefone ou nome. Use antes de
    criar um contato novo, ou antes de decidir mesclar dois contatos.

    Args:
        params (FindDuplicateContactsInput): email, phone, name (ao menos um deve ser informado)
            e exclude_contact_id (opcional).

    Returns:
        str: JSON com a lista de contatos candidatos a duplicata.
    """
    return await run_tool(
        api_get(
            "/contacts/duplicates",
            {
                "email": params.email,
                "phone": params.phone,
                "name": params.name,
                "excludeContactId": params.exclude_contact_id,
            },
        )
    )


@mcp.tool(
    name="entur_merge_contacts",
    annotations={
        "title": "Mesclar contatos duplicados",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_merge_contacts(params: DataInput) -> str:
    """Mescla dois contatos duplicados em um só. A operação é reversível via
    entur_revert_contact_merge. Confirme com o usuário qual contato é o principal
    (que permanece) antes de executar.

    Args:
        params (DataInput): data (dict) com os IDs dos contatos, tipicamente
            {"primaryContactId": "...", "duplicateContactId": "..."}.

    Returns:
        str: JSON com o resultado do merge, incluindo o mergeId para reverter se necessário.
    """
    return await run_tool(api_post("/contacts/merge", params.data))


class RevertMergeInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    merge_id: str = Field(..., description="ID do merge a desfazer, retornado por entur_merge_contacts.", min_length=1)


@mcp.tool(
    name="entur_revert_contact_merge",
    annotations={
        "title": "Desfazer mesclagem de contatos",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_revert_contact_merge(params: RevertMergeInput) -> str:
    """Desfaz uma mesclagem de contatos anterior, restaurando os dois contatos originais.

    Args:
        params (RevertMergeInput): merge_id do merge a reverter.

    Returns:
        str: JSON com o resultado da reversão.
    """
    return await run_tool(api_post(f"/contacts/merge/{params.merge_id}/revert"))


class ContactSubResourceInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(..., description="ID do contato.", min_length=1)
    limit: Optional[int] = Field(default=None, description="Máximo de itens a retornar.", ge=1, le=100)


@mcp.tool(
    name="entur_get_contact_attribution",
    annotations={
        "title": "Ver atribuição de marketing do contato",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_contact_attribution(params: ContactSubResourceInput) -> str:
    """Retorna a atribuição de marketing do contato: por qual UTM/anúncio/origem ele chegou.

    Args:
        params (ContactSubResourceInput): id do contato, limit opcional.

    Returns:
        str: JSON com os eventos de atribuição (UTM, campanha, anúncio) do contato.
    """
    return await run_tool(api_get(f"/contacts/{params.id}/attribution", {"limit": params.limit}))


@mcp.tool(
    name="entur_get_contact_travel_preferences",
    annotations={
        "title": "Ver preferências de viagem do contato",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_contact_travel_preferences(params: IdInput) -> str:
    """Retorna as preferências de viagem e fidelidade cadastradas para o contato.

    Args:
        params (IdInput): id do contato.

    Returns:
        str: JSON com as preferências de viagem do contato.
    """
    return await run_tool(api_get(f"/contacts/{params.id}/travel-preferences"))


@mcp.tool(
    name="entur_set_contact_travel_preferences",
    annotations={
        "title": "Salvar preferências de viagem do contato",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_set_contact_travel_preferences(params: IdWithDataInput) -> str:
    """Grava (upsert) as preferências de viagem do contato, substituindo o valor anterior.

    Args:
        params (IdWithDataInput): id do contato + data (dict) com as preferências
            (ex: classe de voo preferida, tipo de acomodação, destinos favoritos).

    Returns:
        str: JSON com as preferências salvas.
    """
    return await run_tool(api_put(f"/contacts/{params.id}/travel-preferences", params.data))


@mcp.tool(
    name="entur_get_contact_referral_credit",
    annotations={
        "title": "Ver saldo de crédito de indicação",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_contact_referral_credit(params: IdInput) -> str:
    """Retorna o saldo atual de crédito de indicação (referral) do contato.

    Args:
        params (IdInput): id do contato.

    Returns:
        str: JSON com o saldo de crédito de indicação.
    """
    return await run_tool(api_get(f"/contacts/{params.id}/referral-credit"))


@mcp.tool(
    name="entur_get_contact_referral_credit_ledger",
    annotations={
        "title": "Ver extrato de crédito de indicação",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_contact_referral_credit_ledger(params: ContactSubResourceInput) -> str:
    """Retorna o extrato (histórico de lançamentos) de crédito de indicação do contato.

    Args:
        params (ContactSubResourceInput): id do contato, limit opcional.

    Returns:
        str: JSON com a lista de lançamentos do extrato.
    """
    return await run_tool(
        api_get(f"/contacts/{params.id}/referral-credit/ledger", {"limit": params.limit})
    )


@mcp.tool(
    name="entur_add_contact_loyalty_program",
    annotations={
        "title": "Adicionar programa de fidelidade ao contato",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_add_contact_loyalty_program(params: IdWithDataInput) -> str:
    """Vincula um programa de fidelidade (ex: milhagem aérea, pontos de hotel) ao contato.

    Args:
        params (IdWithDataInput): id do contato + data (dict) com os dados do programa
            (ex: {"programName": "...", "memberNumber": "...", "tier": "...", "pointsBalance": 0}).

    Returns:
        str: JSON do vínculo de fidelidade criado, incluindo seu ID (usado em
            entur_update_loyalty_program, entur_adjust_loyalty_points etc.).
    """
    return await run_tool(api_post(f"/contacts/{params.id}/loyalty", params.data))


@mcp.tool(
    name="entur_update_loyalty_program",
    annotations={
        "title": "Editar programa de fidelidade",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_loyalty_program(params: IdWithDataInput) -> str:
    """Edita os dados de um vínculo de programa de fidelidade já existente.

    Args:
        params (IdWithDataInput): id do vínculo de fidelidade (não do contato) + data (dict)
            com os campos a alterar.

    Returns:
        str: JSON do vínculo de fidelidade atualizado.
    """
    return await run_tool(api_patch(f"/loyalty-programs/{params.id}", params.data))


@mcp.tool(
    name="entur_delete_loyalty_program",
    annotations={
        "title": "Remover programa de fidelidade",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_delete_loyalty_program(params: IdInput) -> str:
    """Remove o vínculo de um programa de fidelidade do contato. AÇÃO DESTRUTIVA: confirme
    com o usuário antes de executar.

    Args:
        params (IdInput): id do vínculo de fidelidade a remover.

    Returns:
        str: JSON de confirmação, ou mensagem de erro.
    """
    return await run_tool(api_delete(f"/loyalty-programs/{params.id}"))


@mcp.tool(
    name="entur_adjust_loyalty_points",
    annotations={
        "title": "Ajustar pontos de fidelidade",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_adjust_loyalty_points(params: IdWithDataInput) -> str:
    """Lança um ajuste (crédito ou débito) de pontos num programa de fidelidade do contato.

    Args:
        params (IdWithDataInput): id do vínculo de fidelidade + data (dict), tipicamente
            {"points": 100, "reason": "..."} (use valor negativo para debitar).

    Returns:
        str: JSON com o novo saldo após o ajuste.
    """
    return await run_tool(api_post(f"/loyalty-programs/{params.id}/adjust", params.data))


@mcp.tool(
    name="entur_get_loyalty_ledger",
    annotations={
        "title": "Ver extrato de pontos de fidelidade",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_loyalty_ledger(params: ContactSubResourceInput) -> str:
    """Retorna o extrato (histórico de lançamentos) de pontos de um programa de fidelidade.

    Args:
        params (ContactSubResourceInput): id do vínculo de fidelidade, limit opcional.

    Returns:
        str: JSON com a lista de lançamentos do extrato de pontos.
    """
    return await run_tool(api_get(f"/loyalty-programs/{params.id}/ledger", {"limit": params.limit}))
