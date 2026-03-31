from __future__ import annotations

import httpx
import pytest

from toggl_track_mcp.api import workspaces as api


@pytest.mark.asyncio
async def test_list_workspaces(toggl_client, mock_api, sample_workspace):
    mock_api.get("/api/v9/workspaces").mock(
        return_value=httpx.Response(200, json=[sample_workspace])
    )
    result = await api.list_workspaces(toggl_client)
    assert len(result) == 1
    assert result[0]["name"] == "My Workspace"


@pytest.mark.asyncio
async def test_get_workspace(toggl_client, mock_api, sample_workspace):
    mock_api.get("/api/v9/workspaces/100").mock(
        return_value=httpx.Response(200, json=sample_workspace)
    )
    result = await api.get_workspace(toggl_client, 100)
    assert result["id"] == 100


@pytest.mark.asyncio
async def test_get_me(toggl_client, mock_api, sample_me):
    mock_api.get("/api/v9/me").mock(
        return_value=httpx.Response(200, json=sample_me)
    )
    result = await api.get_me(toggl_client)
    assert result["email"] == "test@example.com"
    assert result["default_workspace_id"] == 100
