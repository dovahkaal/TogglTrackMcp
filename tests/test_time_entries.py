from __future__ import annotations

import httpx
import pytest

from toggl_track_mcp.api import time_entries as api


@pytest.mark.asyncio
async def test_list_time_entries(toggl_client, mock_api, sample_time_entry):
    mock_api.get("/api/v9/me/time_entries").mock(
        return_value=httpx.Response(200, json=[sample_time_entry])
    )
    result = await api.list_time_entries(toggl_client)
    assert len(result) == 1
    assert result[0]["id"] == 12345


@pytest.mark.asyncio
async def test_list_time_entries_with_dates(toggl_client, mock_api, sample_time_entry):
    mock_api.get("/api/v9/me/time_entries").mock(
        return_value=httpx.Response(200, json=[sample_time_entry])
    )
    result = await api.list_time_entries(
        toggl_client, start_date="2024-01-01", end_date="2024-01-31"
    )
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_current_time_entry_running(toggl_client, mock_api, sample_running_entry):
    mock_api.get("/api/v9/me/time_entries/current").mock(
        return_value=httpx.Response(200, json=sample_running_entry)
    )
    result = await api.get_current_time_entry(toggl_client)
    assert result is not None
    assert result["duration"] < 0


@pytest.mark.asyncio
async def test_get_current_time_entry_none(toggl_client, mock_api):
    mock_api.get("/api/v9/me/time_entries/current").mock(
        return_value=httpx.Response(200, json=None)
    )
    result = await api.get_current_time_entry(toggl_client)
    assert result is None


@pytest.mark.asyncio
async def test_create_time_entry(toggl_client, mock_api, sample_time_entry):
    mock_api.post("/api/v9/workspaces/100/time_entries").mock(
        return_value=httpx.Response(200, json=sample_time_entry)
    )
    result = await api.create_time_entry(
        toggl_client,
        workspace_id=100,
        start="2024-01-15T09:00:00Z",
        duration=5400,
        description="Working on feature",
    )
    assert result["id"] == 12345


@pytest.mark.asyncio
async def test_stop_time_entry(toggl_client, mock_api, sample_time_entry):
    mock_api.patch("/api/v9/workspaces/100/time_entries/12346/stop").mock(
        return_value=httpx.Response(200, json=sample_time_entry)
    )
    result = await api.stop_time_entry(toggl_client, 100, 12346)
    assert result["id"] == 12345


@pytest.mark.asyncio
async def test_update_time_entry(toggl_client, mock_api, sample_time_entry):
    updated = {**sample_time_entry, "description": "Updated"}
    mock_api.put("/api/v9/workspaces/100/time_entries/12345").mock(
        return_value=httpx.Response(200, json=updated)
    )
    result = await api.update_time_entry(
        toggl_client, 100, 12345, description="Updated"
    )
    assert result["description"] == "Updated"


@pytest.mark.asyncio
async def test_delete_time_entry(toggl_client, mock_api):
    mock_api.delete("/api/v9/workspaces/100/time_entries/12345").mock(
        return_value=httpx.Response(204)
    )
    result = await api.delete_time_entry(toggl_client, 100, 12345)
    assert result is None
