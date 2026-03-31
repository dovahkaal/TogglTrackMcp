from __future__ import annotations

import httpx
import pytest

from toggl_track_mcp.api import tags as api


@pytest.mark.asyncio
async def test_list_tags(toggl_client, mock_api, sample_tag):
    mock_api.get("/api/v9/workspaces/100/tags").mock(
        return_value=httpx.Response(200, json=[sample_tag])
    )
    result = await api.list_tags(toggl_client, 100)
    assert len(result) == 1
    assert result[0]["name"] == "urgent"


@pytest.mark.asyncio
async def test_create_tag(toggl_client, mock_api, sample_tag):
    mock_api.post("/api/v9/workspaces/100/tags").mock(
        return_value=httpx.Response(200, json=sample_tag)
    )
    result = await api.create_tag(toggl_client, 100, "urgent")
    assert result["name"] == "urgent"


@pytest.mark.asyncio
async def test_update_tag(toggl_client, mock_api, sample_tag):
    updated = {**sample_tag, "name": "critical"}
    mock_api.put("/api/v9/workspaces/100/tags/400").mock(
        return_value=httpx.Response(200, json=updated)
    )
    result = await api.update_tag(toggl_client, 100, 400, "critical")
    assert result["name"] == "critical"


@pytest.mark.asyncio
async def test_delete_tag(toggl_client, mock_api):
    mock_api.delete("/api/v9/workspaces/100/tags/400").mock(
        return_value=httpx.Response(204)
    )
    result = await api.delete_tag(toggl_client, 100, 400)
    assert result is None
