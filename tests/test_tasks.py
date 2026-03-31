from __future__ import annotations

import httpx
import pytest

from toggl_track_mcp.api import tasks as api


@pytest.mark.asyncio
async def test_list_tasks(toggl_client, mock_api, sample_task):
    mock_api.get("/api/v9/workspaces/100/projects/200/tasks").mock(
        return_value=httpx.Response(200, json=[sample_task])
    )
    result = await api.list_tasks(toggl_client, 100, 200)
    assert len(result) == 1
    assert result[0]["name"] == "Design mockups"


@pytest.mark.asyncio
async def test_get_task(toggl_client, mock_api, sample_task):
    mock_api.get("/api/v9/workspaces/100/projects/200/tasks/500").mock(
        return_value=httpx.Response(200, json=sample_task)
    )
    result = await api.get_task(toggl_client, 100, 200, 500)
    assert result["id"] == 500


@pytest.mark.asyncio
async def test_create_task(toggl_client, mock_api, sample_task):
    mock_api.post("/api/v9/workspaces/100/projects/200/tasks").mock(
        return_value=httpx.Response(200, json=sample_task)
    )
    result = await api.create_task(toggl_client, 100, 200, "Design mockups")
    assert result["name"] == "Design mockups"


@pytest.mark.asyncio
async def test_update_task(toggl_client, mock_api, sample_task):
    updated = {**sample_task, "name": "Updated task"}
    mock_api.put("/api/v9/workspaces/100/projects/200/tasks/500").mock(
        return_value=httpx.Response(200, json=updated)
    )
    result = await api.update_task(toggl_client, 100, 200, 500, name="Updated task")
    assert result["name"] == "Updated task"


@pytest.mark.asyncio
async def test_delete_task(toggl_client, mock_api):
    mock_api.delete("/api/v9/workspaces/100/projects/200/tasks/500").mock(
        return_value=httpx.Response(204)
    )
    result = await api.delete_task(toggl_client, 100, 200, 500)
    assert result is None
