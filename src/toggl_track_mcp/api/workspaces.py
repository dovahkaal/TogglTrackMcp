from __future__ import annotations

from typing import Any

from toggl_track_mcp.api.client import TogglClient


async def get_me(client: TogglClient) -> dict[str, Any]:
    return await client.get("/api/v9/me")


async def list_workspaces(client: TogglClient) -> list[dict[str, Any]]:
    return await client.get("/api/v9/workspaces")


async def get_workspace(
    client: TogglClient, workspace_id: int
) -> dict[str, Any]:
    return await client.get(f"/api/v9/workspaces/{workspace_id}")
