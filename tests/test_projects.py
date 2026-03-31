from __future__ import annotations

import httpx
import pytest

from toggl_track_mcp.api import projects as api


@pytest.mark.asyncio
async def test_list_projects(toggl_client, mock_api, sample_project):
    mock_api.get("/api/v9/workspaces/100/projects").mock(
        return_value=httpx.Response(200, json=[sample_project])
    )
    result = await api.list_projects(toggl_client, 100)
    assert len(result) == 1
    assert result[0]["name"] == "My Project"


@pytest.mark.asyncio
async def test_get_project(toggl_client, mock_api, sample_project):
    mock_api.get("/api/v9/workspaces/100/projects/200").mock(
        return_value=httpx.Response(200, json=sample_project)
    )
    result = await api.get_project(toggl_client, 100, 200)
    assert result["id"] == 200


@pytest.mark.asyncio
async def test_create_project(toggl_client, mock_api, sample_project):
    mock_api.post("/api/v9/workspaces/100/projects").mock(
        return_value=httpx.Response(200, json=sample_project)
    )
    result = await api.create_project(toggl_client, 100, "My Project")
    assert result["name"] == "My Project"


@pytest.mark.asyncio
async def test_update_project(toggl_client, mock_api, sample_project):
    updated = {**sample_project, "name": "Renamed"}
    mock_api.put("/api/v9/workspaces/100/projects/200").mock(
        return_value=httpx.Response(200, json=updated)
    )
    result = await api.update_project(toggl_client, 100, 200, name="Renamed")
    assert result["name"] == "Renamed"


@pytest.mark.asyncio
async def test_delete_project(toggl_client, mock_api):
    mock_api.delete("/api/v9/workspaces/100/projects/200").mock(
        return_value=httpx.Response(204)
    )
    result = await api.delete_project(toggl_client, 100, 200)
    assert result is None
