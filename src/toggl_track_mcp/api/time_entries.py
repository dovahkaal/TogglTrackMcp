from __future__ import annotations

from typing import Any

from toggl_track_mcp.api.client import TogglClient


async def list_time_entries(
    client: TogglClient,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    return await client.get("/api/v9/me/time_entries", params=params)


async def get_current_time_entry(
    client: TogglClient,
) -> dict[str, Any] | None:
    return await client.get("/api/v9/me/time_entries/current")


async def get_time_entry(
    client: TogglClient, time_entry_id: int
) -> dict[str, Any]:
    return await client.get(f"/api/v9/me/time_entries/{time_entry_id}")


async def create_time_entry(
    client: TogglClient,
    workspace_id: int,
    start: str,
    duration: int,
    description: str | None = None,
    project_id: int | None = None,
    task_id: int | None = None,
    billable: bool = False,
    tags: list[str] | None = None,
    tag_ids: list[int] | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "workspace_id": workspace_id,
        "start": start,
        "duration": duration,
        "created_with": "toggl-track-mcp",
        "billable": billable,
    }
    if description is not None:
        body["description"] = description
    if project_id is not None:
        body["project_id"] = project_id
    if task_id is not None:
        body["task_id"] = task_id
    if tags is not None:
        body["tags"] = tags
    if tag_ids is not None:
        body["tag_ids"] = tag_ids
    return await client.post(
        f"/api/v9/workspaces/{workspace_id}/time_entries", json=body
    )


async def update_time_entry(
    client: TogglClient,
    workspace_id: int,
    time_entry_id: int,
    **fields: Any,
) -> dict[str, Any]:
    return await client.put(
        f"/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}",
        json=fields,
    )


async def delete_time_entry(
    client: TogglClient, workspace_id: int, time_entry_id: int
) -> None:
    await client.delete(
        f"/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}"
    )


async def stop_time_entry(
    client: TogglClient, workspace_id: int, time_entry_id: int
) -> dict[str, Any]:
    return await client.patch(
        f"/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}/stop"
    )
