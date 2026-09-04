"""Helpers for running blocking external I/O without blocking the event loop."""

import asyncio
from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")

DEFAULT_EXTERNAL_IO_TIMEOUT = 30.0


class ExternalIOError(RuntimeError):
    """An external blocking operation failed or exceeded its time budget."""


async def run_blocking_io(
    operation: Callable[[], T],
    *,
    operation_name: str,
    timeout: float = DEFAULT_EXTERNAL_IO_TIMEOUT,
) -> T:
    """Run a synchronous operation in a worker thread with a bounded wait."""
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")

    try:
        return await asyncio.wait_for(asyncio.to_thread(operation), timeout=timeout)
    except asyncio.TimeoutError as error:
        raise ExternalIOError(
            f"{operation_name} timed out after {timeout:.1f} seconds"
        ) from error
    except Exception as error:
        raise ExternalIOError(f"{operation_name} failed: {error}") from error
