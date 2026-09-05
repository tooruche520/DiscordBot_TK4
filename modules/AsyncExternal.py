"""Helpers for running blocking external I/O without blocking the event loop."""

import asyncio
from collections.abc import Callable
import threading
from typing import TypeVar


T = TypeVar("T")

DEFAULT_EXTERNAL_IO_TIMEOUT = 30.0

_active_operation_keys: set[str] = set()
_active_operation_keys_lock = threading.Lock()


class ExternalIOError(RuntimeError):
    """An external blocking operation failed or exceeded its time budget."""


async def run_blocking_io(
    operation: Callable[[], T],
    *,
    operation_name: str,
    operation_key: str | None = None,
    timeout: float = DEFAULT_EXTERNAL_IO_TIMEOUT,
) -> T:
    """Run a synchronous operation in a worker thread with a bounded wait.

    A timed-out thread cannot be forcefully stopped by asyncio. The operation
    key keeps a still-running worker from being started again until that worker
    exits, preventing repeated scheduled calls from piling up. When callers do
    not provide a key, a name prefix before ``" for "`` is used so operations
    such as per-article Gemini translations still share one stable key.
    """
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")

    active_key = operation_key or operation_name.split(" for ", 1)[0]
    with _active_operation_keys_lock:
        if active_key in _active_operation_keys:
            raise ExternalIOError(
                f"{operation_name} skipped because a previous operation is still running"
            )
        _active_operation_keys.add(active_key)

    def run_and_release_key() -> T:
        try:
            return operation()
        finally:
            with _active_operation_keys_lock:
                _active_operation_keys.discard(active_key)

    try:
        return await asyncio.wait_for(
            asyncio.to_thread(run_and_release_key), timeout=timeout
        )
    except asyncio.TimeoutError as error:
        raise ExternalIOError(
            f"{operation_name} timed out after {timeout:.1f} seconds"
        ) from error
    except Exception as error:
        raise ExternalIOError(f"{operation_name} failed: {error}") from error
