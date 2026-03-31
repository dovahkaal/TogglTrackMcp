from __future__ import annotations

import httpx
import pytest

from toggl_track_mcp.api import clients as api


@pytest.mark.asyncio
async def test_list_clients(toggl_client, mock_api, sample_client_entity):
    mock_api.get("/api/v9/workspaces/100/clients").mock(
        return_value=httpx.Response(200, json=[sample_client_entity])
    )
    result = await api.list_clients(toggl_client, 100)
    assert len(result) == 1
    assert result[0]["name"] == "Acme Corp"


@pytest.mark.asyncio
async def test_create_client(toggl_client, mock_api, sample_client_entity):
    mock_api.post("/api/v9/workspaces/100/clients").mock(
        return_value=httpx.Response(200, json=sample_client_entity)
    )
    result = await api.create_client(toggl_client, 100, "Acme Corp")
    assert result["name"] == "Acme Corp"


@pytest.mark.asyncio
async def test_update_client(toggl_client, mock_api, sample_client_entity):
    updated = {**sample_client_entity, "name": "Acme Inc"}
    mock_api.put("/api/v9/workspaces/100/clients/300").mock(
        return_value=httpx.Response(200, json=updated)
    )
    result = await api.update_client(toggl_client, 100, 300, name="Acme Inc")
    assert result["name"] == "Acme Inc"


@pytest.mark.asyncio
async def test_delete_client(toggl_client, mock_api):
    mock_api.delete("/api/v9/workspaces/100/clients/300").mock(
        return_value=httpx.Response(204)
    )
    result = await api.delete_client(toggl_client, 100, 300)
    assert result is None


@pytest.mark.asyncio
async def test_archive_client(toggl_client, mock_api):
    mock_api.post("/api/v9/workspaces/100/clients/300/archive").mock(
        return_value=httpx.Response(200, json=[300])
    )
    result = await api.archive_client(toggl_client, 100, 300)
    assert result == [300]


@pytest.mark.asyncio
async def test_restore_client(toggl_client, mock_api, sample_client_entity):
    mock_api.post("/api/v9/workspaces/100/clients/300/restore").mock(
        return_value=httpx.Response(200, json=sample_client_entity)
    )
    result = await api.restore_client(toggl_client, 100, 300)
    assert result["name"] == "Acme Corp"
