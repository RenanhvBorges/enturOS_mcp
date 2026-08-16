"""Ferramentas de Tarefas do EnturOS CRM."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from ..client import api_get, api_patch, api_post
from ..core import mcp
from ..models import DataInput, IdInput, IdWithDataInput
from ..utils import run_tool


class ListTasksInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    limit: Optional[int] = Field(default=50, description="Máximo de itens a retornar.", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="Itens a pular, para paginação.", ge=0)
    status: Optional[str] = Field(default=None, description="Filtra por status da tarefa (ex: 'open', 'done').")


@mcp.tool(
    name="entur_list_tasks",
    annotations={
        "title": "Listar tarefas",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_list_tasks(params: ListTasksInput) -> str:
    """Lista as tarefas da empresa, com filtro de status e paginação.

    Args:
        params (ListTasksInput): limit, offset, status (opcional).

    Returns:
        str: JSON com "data" (lista de tarefas) e "totalCount".
    """
    return await run_tool(
        api_get("/tasks", {"limit": params.limit, "offset": params.offset, "status": params.status})
    )


@mcp.tool(
    name="entur_create_task",
    annotations={
        "title": "Criar tarefa",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def entur_create_task(params: DataInput) -> str:
    """Cria uma nova tarefa, opcionalmente vinculada a um contato ou negociação.

    Args:
        params (DataInput): data (dict) com os campos da tarefa. Campos típicos: title
            (obrigatório), dueDate (ISO 8601), assigneeId, contactId, dealId.

    Returns:
        str: JSON da tarefa criada.
    """
    return await run_tool(api_post("/tasks", params.data))


@mcp.tool(
    name="entur_get_task",
    annotations={
        "title": "Obter tarefa por ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_get_task(params: IdInput) -> str:
    """Obtém os dados completos de uma tarefa pelo ID.

    Args:
        params (IdInput): id da tarefa.

    Returns:
        str: JSON da tarefa, ou mensagem de erro se não existir.
    """
    return await run_tool(api_get(f"/tasks/{params.id}"))


@mcp.tool(
    name="entur_update_task",
    annotations={
        "title": "Atualizar/concluir tarefa",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def entur_update_task(params: IdWithDataInput) -> str:
    """Atualiza uma tarefa. Definir data={"status": "done"} conclui a tarefa.

    Args:
        params (IdWithDataInput): id da tarefa + data (dict) com os campos a alterar
            (ex: {"status": "done"}, {"dueDate": "..."}, {"assigneeId": "..."}).

    Returns:
        str: JSON da tarefa atualizada.
    """
    return await run_tool(api_patch(f"/tasks/{params.id}", params.data))
