from __future__ import annotations

from typing import Any

from toggl_track_mcp.api.client import TogglClient


async def list_projects(
    client: TogglClient,
    workspace_id: int,
    active: bool | None = None,
    name: str | None = None,
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {}
    if active is not None:
        params["active"] = str(active).lower()
    if name is not None:
        params["name"] = name
    return await client.get(
        f"/api/v9/workspaces/{workspace_id}/projects", params=params
    )


async def get_project(
    client: TogglClient, workspace_id: int, project_id: int
) -> dict[str, Any]:
    return await client.get(
        f"/api/v9/workspaces/{workspace_id}/projects/{project_id}"
    )


async def create_project(
    client: TogglClient,
    workspace_id: int,
    name: str,
    client_id: int | None = None,
    color: str | None = None,
    billable: bool | None = None,
    is_private: bool | None = None,
    estimated_hours: int | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name}
    if client_id is not None:
        body["client_id"] = client_id
    if color is not None:
        body["color"] = color
    if billable is not None:
        body["billable"] = billable
    if is_private is not None:
        body["is_private"] = is_private
    if estimated_hours is not None:
        body["estimated_hours"] = estimated_hours
    return await client.post(
        f"/api/v9/workspaces/{workspace_id}/projects", json=body
    )


async def update_project(
    client: TogglClient,
    workspace_id: int,
    project_id: int,
    **fields: Any,
) -> dict[str, Any]:
    return await client.put(
        f"/api/v9/workspaces/{workspace_id}/projects/{project_id}",
        json=fields,
    )


async def delete_project(
    client: TogglClient, workspace_id: int, project_id: int
) -> None:
    await client.delete(
        f"/api/v9/workspaces/{workspace_id}/projects/{project_id}"
    )
