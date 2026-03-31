from __future__ import annotations

import pytest
import respx
import httpx

from toggl_track_mcp.api.client import TogglClient


@pytest.fixture
def mock_api():
    with respx.mock(base_url="https://api.track.toggl.com") as rsps:
        yield rsps


@pytest.fixture
def toggl_client():
    client = TogglClient(api_token="test_token_123")
    client._last_request_time = 0
    return client


@pytest.fixture
def sample_time_entry():
    return {
        "id": 12345,
        "workspace_id": 100,
        "project_id": 200,
        "description": "Working on feature",
        "start": "2024-01-15T09:00:00Z",
        "stop": "2024-01-15T10:30:00Z",
        "duration": 5400,
        "billable": False,
        "tags": ["dev"],
    }


@pytest.fixture
def sample_running_entry():
    return {
        "id": 12346,
        "workspace_id": 100,
        "description": "In progress",
        "start": "2024-01-15T14:00:00Z",
        "duration": -1705323600,
        "billable": False,
        "tags": [],
    }


@pytest.fixture
def sample_project():
    return {
        "id": 200,
        "workspace_id": 100,
        "name": "My Project",
        "active": True,
        "billable": False,
        "color": "#FF0000",
    }


@pytest.fixture
def sample_client_entity():
    return {
        "id": 300,
        "workspace_id": 100,
        "name": "Acme Corp",
        "notes": "Important client",
    }


@pytest.fixture
def sample_tag():
    return {
        "id": 400,
        "workspace_id": 100,
        "name": "urgent",
    }


@pytest.fixture
def sample_task():
    return {
        "id": 500,
        "project_id": 200,
        "workspace_id": 100,
        "name": "Design mockups",
        "active": True,
        "estimated_seconds": 7200,
    }


@pytest.fixture
def sample_workspace():
    return {
        "id": 100,
        "name": "My Workspace",
        "premium": False,
    }


@pytest.fixture
def sample_me():
    return {
        "id": 1,
        "email": "test@example.com",
        "default_workspace_id": 100,
        "timezone": "America/New_York",
    }
