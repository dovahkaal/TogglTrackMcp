from __future__ import annotations

from typing import Any

from toggl_track_mcp.api.client import TogglClient


async def list_tasks(
    client: TogglClient,
    workspace_id: int,
    project_id: int,
) -> list[dict[str, Any]]:
    return await client.get(
        f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks"
    )


async def get_task(
    client: TogglClient,
    workspace_id: int,
    project_id: int,
    task_id: int,
) -> dict[str, Any]:
    return await client.get(
        f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}"
    )


async def create_task(
    client: TogglClient,
    workspace_id: int,
    project_id: int,
    name: str,
    estimated_seconds: int | None = None,
    user_id: int | None = None,
    active: bool | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name}
    if estimated_seconds is not None:
        body["estimated_seconds"] = estimated_seconds
    if user_id is not None:
        body["user_id"] = user_id
    if active is not None:
        body["active"] = active
    return await client.post(
        f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks",
        json=body,
    )


async def update_task(
    client: TogglClient,
    workspace_id: int,
    project_id: int,
    task_id: int,
    **fields: Any,
) -> dict[str, Any]:
    return await client.put(
        f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}",
        json=fields,
    )


async def delete_task(
    client: TogglClient,
    workspace_id: int,
    project_id: int,
    task_id: int,
) -> None:
    await client.delete(
        f"/api/v9/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}"
    )
