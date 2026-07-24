"""Thread-safe bridge between verification workers and SSE consumers."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable


ProgressCallback = Callable[[str, str, str, dict[str, Any]], None]


@dataclass(frozen=True)
class ProgressEvent:
    stage: str
    event: str
    message: str
    snapshot: dict[str, Any] = field(default_factory=dict)


class AsyncProgressBridge:
    """Accept worker-thread callbacks and expose them to an async SSE loop."""

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop
        self._queue: asyncio.Queue[ProgressEvent] = asyncio.Queue()

    def publish(self, stage: str, event: str, message: str, snapshot: dict[str, Any] | None = None) -> None:
        self._loop.call_soon_threadsafe(
            self._queue.put_nowait,
            ProgressEvent(stage=stage, event=event, message=message, snapshot=snapshot or {}),
        )

    async def next(self, timeout: float = 0.1) -> ProgressEvent | None:
        try:
            return await asyncio.wait_for(self._queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    def drain(self) -> list[ProgressEvent]:
        events: list[ProgressEvent] = []
        while not self._queue.empty():
            events.append(self._queue.get_nowait())
        return events
