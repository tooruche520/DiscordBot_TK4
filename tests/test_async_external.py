import asyncio
import threading
import unittest

from modules.AsyncExternal import ExternalIOError, run_blocking_io


class RunBlockingIOTests(unittest.IsolatedAsyncioTestCase):
    async def test_blocking_operation_does_not_pause_event_loop(self):
        started = threading.Event()
        release = threading.Event()
        heartbeat_count = 0

        def blocking_operation():
            started.set()
            release.wait(timeout=1)
            return "complete"

        async def heartbeat():
            nonlocal heartbeat_count
            while not release.is_set():
                heartbeat_count += 1
                await asyncio.sleep(0)

        heartbeat_task = asyncio.create_task(heartbeat())
        operation_task = asyncio.create_task(
            run_blocking_io(
                blocking_operation,
                operation_name="slow RSS update",
                timeout=1,
            )
        )

        try:
            await asyncio.to_thread(started.wait, 1)
            await asyncio.sleep(0.01)
            self.assertGreater(heartbeat_count, 0)
            release.set()
            self.assertEqual(await operation_task, "complete")
        finally:
            release.set()
            heartbeat_task.cancel()
            await asyncio.gather(heartbeat_task, return_exceptions=True)
            await asyncio.gather(operation_task, return_exceptions=True)

    async def test_timeout_is_bounded_and_reported(self):
        started = threading.Event()
        release = threading.Event()

        def blocking_operation():
            started.set()
            release.wait(timeout=1)

        operation_task = asyncio.create_task(
            run_blocking_io(
                blocking_operation,
                operation_name="Gemini translation",
                timeout=0.01,
            )
        )

        try:
            await asyncio.to_thread(started.wait, 1)
            with self.assertRaisesRegex(ExternalIOError, "Gemini translation"):
                await operation_task
        finally:
            release.set()
            await asyncio.gather(operation_task, return_exceptions=True)

    async def test_operation_failure_is_reported(self):
        def failing_operation():
            raise OSError("service unavailable")

        with self.assertRaisesRegex(ExternalIOError, "RSS feed update") as context:
            await run_blocking_io(
                failing_operation,
                operation_name="RSS feed update",
                timeout=1,
            )

        self.assertIsInstance(context.exception.__cause__, OSError)


if __name__ == "__main__":
    unittest.main()
