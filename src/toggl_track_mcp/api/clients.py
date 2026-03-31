from __future__ import annotations

from typing import Any

from toggl_track_mcp.api.client import TogglClient


async def list_clients(
    client: TogglClient,
    workspace_id: int,
    status: str | None = None,
    name: str | None = None,
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {}
    if status is not None:
        params["status"] = status
    if name is not None:
        params["name"] = name
    return await client.get(
        f"/api/v9/workspaces/{workspace_id}/clients", params=params
    )


async def get_client(
    client: TogglClient, workspace_id: int, client_id: int
) -> dict[str, Any]:
    return await client.get(
        f"/api/v9/workspaces/{workspace_id}/clients/{client_id}"
    )


async def create_client(
    client: TogglClient,
    workspace_id: int,
    name: str,
    notes: str | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name, "wid": workspace_id}
    if notes is not None:
        body["notes"] = notes
    return await client.post(
        f"/api/v9/workspaces/{workspace_id}/clients", json=body
    )


async def update_client(
    client: TogglClient,
    workspace_id: int,
    client_id: int,
    name: str | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if notes is not None:
        body["notes"] = notes
    return await client.put(
        f"/api/v9/workspaces/{workspace_id}/clients/{client_id}", json=body
    )


async def delete_client(
    client: TogglClient, workspace_id: int, client_id: int
) -> None:
    await client.delete(
        f"/api/v9/workspaces/{workspace_id}/clients/{client_id}"
    )


async def archive_client(
    client: TogglClient, workspace_id: int, client_id: int
) -> Any:
    return await client.post(
        f"/api/v9/workspaces/{workspace_id}/clients/{client_id}/archive"
    )


async def restore_client(
    client: TogglClient, workspace_id: int, client_id: int
) -> Any:
    return await client.post(
        f"/api/v9/workspaces/{workspace_id}/clients/{client_id}/restore"
    )
