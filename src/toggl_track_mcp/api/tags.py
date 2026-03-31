from __future__ import annotations

from typing import Any

from toggl_track_mcp.api.client import TogglClient


async def list_tags(
    client: TogglClient, workspace_id: int
) -> list[dict[str, Any]]:
    return await client.get(f"/api/v9/workspaces/{workspace_id}/tags")


async def create_tag(
    client: TogglClient, workspace_id: int, name: str
) -> dict[str, Any]:
    return await client.post(
        f"/api/v9/workspaces/{workspace_id}/tags", json={"name": name}
    )


async def update_tag(
    client: TogglClient, workspace_id: int, tag_id: int, name: str
) -> dict[str, Any]:
    return await client.put(
        f"/api/v9/workspaces/{workspace_id}/tags/{tag_id}",
        json={"name": name},
    )


async def delete_tag(
    client: TogglClient, workspace_id: int, tag_id: int
) -> None:
    await client.delete(f"/api/v9/workspaces/{workspace_id}/tags/{tag_id}")
