from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP

from toggl_track_mcp.api import TogglClient


@dataclass
class AppContext:
    toggl: TogglClient


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    api_token = os.environ.get("TOGGL_API_TOKEN")
    if not api_token:
        raise ValueError(
            "TOGGL_API_TOKEN environment variable is required. "
            "Get your API token from https://track.toggl.com/profile"
        )
    client = TogglClient(api_token)
    try:
        yield AppContext(toggl=client)
    finally:
        await client.close()


mcp = FastMCP(
    name="toggl-track",
    lifespan=lifespan,
)

# Import tool modules to register @mcp.tool() decorators
import toggl_track_mcp.tools.workspaces  # noqa: E402, F401
import toggl_track_mcp.tools.time_entries  # noqa: E402, F401
import toggl_track_mcp.tools.projects  # noqa: E402, F401
import toggl_track_mcp.tools.clients  # noqa: E402, F401
import toggl_track_mcp.tools.tags  # noqa: E402, F401
import toggl_track_mcp.tools.tasks  # noqa: E402, F401
import toggl_track_mcp.tools.reports  # noqa: E402, F401
