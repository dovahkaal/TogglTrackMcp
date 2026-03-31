from __future__ import annotations

import httpx
import pytest

from toggl_track_mcp.api import reports as api


@pytest.fixture
def sample_summary_report():
    return {
        "groups": [
            {
                "id": 200,
                "sub_groups": [{"title": "Task 1", "seconds": 3600}],
            }
        ],
    }


@pytest.fixture
def sample_detailed_report():
    return [
        {
            "id": 12345,
            "description": "Working",
            "time_entries": [{"seconds": 5400, "start": "2024-01-15T09:00:00Z"}],
        }
    ]


@pytest.fixture
def sample_weekly_report():
    return [
        {
            "user_id": 1,
            "project_id": 200,
            "seconds": [0, 3600, 7200, 0, 0, 0, 0],
        }
    ]


@pytest.mark.asyncio
async def test_get_summary_report(toggl_client, mock_api, sample_summary_report):
    mock_api.post("/reports/api/v3/workspace/100/summary/time_entries").mock(
        return_value=httpx.Response(200, json=sample_summary_report)
    )
    result = await api.get_summary_report(
        toggl_client, 100, "2024-01-01", "2024-01-31"
    )
    assert "groups" in result


@pytest.mark.asyncio
async def test_search_detailed_report(toggl_client, mock_api, sample_detailed_report):
    mock_api.post("/reports/api/v3/workspace/100/search/time_entries").mock(
        return_value=httpx.Response(200, json=sample_detailed_report)
    )
    result = await api.search_detailed_report(
        toggl_client, 100, "2024-01-01", "2024-01-31"
    )
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_weekly_report(toggl_client, mock_api, sample_weekly_report):
    mock_api.post("/reports/api/v3/workspace/100/weekly/time_entries").mock(
        return_value=httpx.Response(200, json=sample_weekly_report)
    )
    result = await api.get_weekly_report(
        toggl_client, 100, "2024-01-01", "2024-01-07"
    )
    assert len(result) == 1
