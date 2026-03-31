from __future__ import annotations

import os
from unittest.mock import patch

import httpx
import pytest
import respx

from toggl_track_mcp.api.client import (
    TogglAuthError,
    TogglClient,
    TogglNotFoundError,
    TogglRateLimitError,
    TogglAPIError,
)


@pytest.mark.asyncio
async def test_get_success(toggl_client, mock_api):
    mock_api.get("/api/v9/me").mock(
        return_value=httpx.Response(200, json={"id": 1, "email": "test@example.com"})
    )
    result = await toggl_client.get("/api/v9/me")
    assert result["id"] == 1


@pytest.mark.asyncio
async def test_auth_error(toggl_client, mock_api):
    mock_api.get("/api/v9/me").mock(
        return_value=httpx.Response(403, text="Forbidden")
    )
    with pytest.raises(TogglAuthError):
        await toggl_client.get("/api/v9/me")


@pytest.mark.asyncio
async def test_not_found_error(toggl_client, mock_api):
    mock_api.get("/api/v9/workspaces/999/projects/1").mock(
        return_value=httpx.Response(404, text="Not found")
    )
    with pytest.raises(TogglNotFoundError):
        await toggl_client.get("/api/v9/workspaces/999/projects/1")


@pytest.mark.asyncio
async def test_rate_limit_error(toggl_client, mock_api):
    mock_api.get("/api/v9/me").mock(
        return_value=httpx.Response(429, headers={"Retry-After": "5"})
    )
    with pytest.raises(TogglRateLimitError) as exc_info:
        await toggl_client.get("/api/v9/me")
    assert exc_info.value.retry_after == 5.0


@pytest.mark.asyncio
async def test_generic_api_error(toggl_client, mock_api):
    mock_api.get("/api/v9/me").mock(
        return_value=httpx.Response(500, text="Internal Server Error")
    )
    with pytest.raises(TogglAPIError) as exc_info:
        await toggl_client.get("/api/v9/me")
    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_delete_returns_none(toggl_client, mock_api):
    mock_api.delete("/api/v9/workspaces/100/time_entries/1").mock(
        return_value=httpx.Response(204)
    )
    result = await toggl_client.delete("/api/v9/workspaces/100/time_entries/1")
    assert result is None


@pytest.mark.asyncio
async def test_get_default_workspace_id_from_env(toggl_client):
    with patch.dict(os.environ, {"TOGGL_WORKSPACE_ID": "42"}):
        toggl_client._default_workspace_id = None
        wid = await toggl_client.get_default_workspace_id()
        assert wid == 42


@pytest.mark.asyncio
async def test_get_default_workspace_id_from_api(toggl_client, mock_api, sample_me):
    mock_api.get("/api/v9/me").mock(
        return_value=httpx.Response(200, json=sample_me)
    )
    with patch.dict(os.environ, {}, clear=True):
        toggl_client._default_workspace_id = None
        wid = await toggl_client.get_default_workspace_id()
        assert wid == 100


@pytest.mark.asyncio
async def test_get_default_workspace_id_cached(toggl_client):
    toggl_client._default_workspace_id = 999
    wid = await toggl_client.get_default_workspace_id()
    assert wid == 999
