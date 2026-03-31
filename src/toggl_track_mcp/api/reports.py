from __future__ import annotations

from typing import Any

from toggl_track_mcp.api.client import TogglClient


async def get_summary_report(
    client: TogglClient,
    workspace_id: int,
    start_date: str,
    end_date: str,
    project_ids: list[int] | None = None,
    client_ids: list[int] | None = None,
    tag_ids: list[int] | None = None,
    billable: bool | None = None,
    grouping: str | None = None,
    sub_grouping: str | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "start_date": start_date,
        "end_date": end_date,
    }
    if project_ids is not None:
        body["project_ids"] = project_ids
    if client_ids is not None:
        body["client_ids"] = client_ids
    if tag_ids is not None:
        body["tag_ids"] = tag_ids
    if billable is not None:
        body["billable"] = billable
    if grouping is not None:
        body["grouping"] = grouping
    if sub_grouping is not None:
        body["sub_grouping"] = sub_grouping
    return await client.post(
        f"/reports/api/v3/workspace/{workspace_id}/summary/time_entries",
        json=body,
    )


async def search_detailed_report(
    client: TogglClient,
    workspace_id: int,
    start_date: str,
    end_date: str,
    description: str | None = None,
    project_ids: list[int] | None = None,
    client_ids: list[int] | None = None,
    tag_ids: list[int] | None = None,
    billable: bool | None = None,
    page_size: int = 50,
    first_row_number: int | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "start_date": start_date,
        "end_date": end_date,
        "page_size": page_size,
    }
    if description is not None:
        body["description"] = description
    if project_ids is not None:
        body["project_ids"] = project_ids
    if client_ids is not None:
        body["client_ids"] = client_ids
    if tag_ids is not None:
        body["tag_ids"] = tag_ids
    if billable is not None:
        body["billable"] = billable
    if first_row_number is not None:
        body["first_row_number"] = first_row_number
    return await client.post(
        f"/reports/api/v3/workspace/{workspace_id}/search/time_entries",
        json=body,
    )


async def get_weekly_report(
    client: TogglClient,
    workspace_id: int,
    start_date: str,
    end_date: str,
    project_ids: list[int] | None = None,
    user_ids: list[int] | None = None,
    billable: bool | None = None,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "start_date": start_date,
        "end_date": end_date,
    }
    if project_ids is not None:
        body["project_ids"] = project_ids
    if user_ids is not None:
        body["user_ids"] = user_ids
    if billable is not None:
        body["billable"] = billable
    return await client.post(
        f"/reports/api/v3/workspace/{workspace_id}/weekly/time_entries",
        json=body,
    )
