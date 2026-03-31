from __future__ import annotations

import asyncio
import os
import time
from typing import Any

import httpx


class TogglAPIError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"Toggl API error {status_code}: {message}")


class TogglAuthError(TogglAPIError):
    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(403, message)


class TogglNotFoundError(TogglAPIError):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(404, message)


class TogglRateLimitError(TogglAPIError):
    def __init__(self, retry_after: float = 1.0) -> None:
        self.retry_after = retry_after
        super().__init__(429, f"Rate limited. Retry after {retry_after}s")


class TogglClient:
    BASE_URL = "https://api.track.toggl.com"

    def __init__(self, api_token: str) -> None:
        self._http = httpx.AsyncClient(
            base_url=self.BASE_URL,
            auth=(api_token, "api_token"),
            headers={"Content-Type": "application/json"},
            timeout=30.0,
        )
        self._semaphore = asyncio.Semaphore(1)
        self._last_request_time: float = 0
        self._default_workspace_id: int | None = None

    async def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < 1.0:
            await asyncio.sleep(1.0 - elapsed)
        self._last_request_time = time.monotonic()

    async def _request(
        self,
        method: str,
        path: str,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        async with self._semaphore:
            await self._throttle()
            response = await self._http.request(
                method, path, json=json, params=params
            )

        if response.status_code in (401, 403):
            raise TogglAuthError()
        if response.status_code == 404:
            text = response.text
            raise TogglNotFoundError(text or "Resource not found")
        if response.status_code == 429:
            retry_after = float(
                response.headers.get("Retry-After", "1")
            )
            raise TogglRateLimitError(retry_after)
        if response.status_code >= 400:
            raise TogglAPIError(response.status_code, response.text)

        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    async def get(self, path: str, **kwargs: Any) -> Any:
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Any:
        return await self._request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> Any:
        return await self._request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> Any:
        return await self._request("PATCH", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Any:
        return await self._request("DELETE", path, **kwargs)

    async def get_default_workspace_id(self) -> int:
        if self._default_workspace_id is not None:
            return self._default_workspace_id

        env_wid = os.environ.get("TOGGL_WORKSPACE_ID")
        if env_wid:
            self._default_workspace_id = int(env_wid)
            return self._default_workspace_id

        me = await self.get("/api/v9/me")
        self._default_workspace_id = me["default_workspace_id"]
        return self._default_workspace_id

    async def close(self) -> None:
        await self._http.aclose()
