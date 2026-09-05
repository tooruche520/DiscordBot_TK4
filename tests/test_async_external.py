import asyncio
import importlib.util
import logging
from pathlib import Path
import sys
import threading
import types
import unittest
from unittest.mock import patch

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
                operation_key="slow-rss-heartbeat",
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
                operation_key="gemini-timeout",
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

    async def test_timeout_blocks_duplicate_until_worker_finishes(self):
        started = threading.Event()
        release = threading.Event()
        finished = threading.Event()
        call_count = 0

        def blocking_operation():
            nonlocal call_count
            call_count += 1
            started.set()
            try:
                release.wait(timeout=1)
            finally:
                finished.set()

        try:
            with self.assertRaisesRegex(ExternalIOError, "timed out"):
                await run_blocking_io(
                    blocking_operation,
                    operation_name="RSS feed update",
                    operation_key="rss-lifecycle",
                    timeout=0.01,
                )

            self.assertTrue(started.is_set())
            with self.assertRaisesRegex(ExternalIOError, "still running"):
                await run_blocking_io(
                    blocking_operation,
                    operation_name="RSS feed update",
                    operation_key="rss-lifecycle",
                    timeout=0.1,
                )
            self.assertEqual(call_count, 1)

            release.set()
            self.assertTrue(await asyncio.to_thread(finished.wait, 1))
            self.assertEqual(
                await run_blocking_io(
                    lambda: "retry succeeds",
                    operation_name="RSS feed update",
                    operation_key="rss-lifecycle",
                    timeout=0.1,
                ),
                "retry succeeds",
            )
        finally:
            release.set()
            await asyncio.to_thread(finished.wait, 1)

    async def test_operation_failure_is_reported(self):
        def failing_operation():
            raise OSError("service unavailable")

        with self.assertRaisesRegex(ExternalIOError, "RSS feed update") as context:
            await run_blocking_io(
                failing_operation,
                operation_name="RSS feed update",
                operation_key="rss-failure",
                timeout=1,
            )

        self.assertIsInstance(context.exception.__cause__, OSError)


class FakeEntry:
    def __init__(self):
        self.title = "測試文章"
        self.link = "https://example.com/article"
        self.summary = "測試摘要"
        self.read = False


class FakeReader:
    def __init__(self, entry, update_feeds=None):
        self.entry = entry
        self.update_feeds_impl = update_feeds
        self.update_calls = 0
        self.marked_entries = []

    def update_feeds(self):
        self.update_calls += 1
        if self.update_feeds_impl is not None:
            return self.update_feeds_impl()

    def get_entries(self, *, feed, limit):
        return [self.entry]

    def mark_entry_as_read(self, entry):
        entry.read = True
        self.marked_entries.append(entry)


class FakeChannel:
    name = "測試頻道"

    def __init__(self):
        self.messages = []

    async def send(self, *, content):
        self.messages.append(content)


class FakeBot:
    def __init__(self, channel):
        self.channel = channel

    def get_channel(self, channel_id):
        return self.channel


class FakeGeminiModels:
    def __init__(self, generate_content):
        self.generate_content_impl = generate_content
        self.calls = []

    def generate_content(self, *, model, contents):
        self.calls.append((model, contents))
        return self.generate_content_impl()


class FakeGeminiClient:
    def __init__(self, generate_content):
        self.models = FakeGeminiModels(generate_content)


def load_rss_module():
    discord = types.ModuleType("discord")
    discord_ext = types.ModuleType("discord.ext")
    commands = types.ModuleType("discord.ext.commands")
    tasks = types.ModuleType("discord.ext.tasks")

    class Cog:
        pass

    class Loop:
        def __init__(self, coroutine):
            self.coro = coroutine

        def before_loop(self, coroutine):
            return coroutine

        def start(self):
            return None

        def cancel(self):
            return None

    def loop(**kwargs):
        def decorator(coroutine):
            return Loop(coroutine)

        return decorator

    commands.Cog = Cog
    tasks.loop = loop
    discord.ext = discord_ext
    discord_ext.commands = commands
    discord_ext.tasks = tasks

    reader = types.ModuleType("reader")
    reader.make_reader = lambda db_path: None

    genai = types.ModuleType("google.genai")
    genai.Client = lambda: FakeGeminiClient(lambda: types.SimpleNamespace(text=""))
    google = types.ModuleType("google")
    google.genai = genai

    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda: None

    fake_modules = {
        "discord": discord,
        "discord.ext": discord_ext,
        "discord.ext.commands": commands,
        "discord.ext.tasks": tasks,
        "reader": reader,
        "google": google,
        "google.genai": genai,
        "dotenv": dotenv,
    }
    module_path = Path(__file__).resolve().parents[1] / "cogs" / "RSSFeed.py"
    spec = importlib.util.spec_from_file_location("rss_feed_under_test", module_path)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake_modules):
        spec.loader.exec_module(module)
    return module


class RSSFeedCallSiteTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.rss_module = load_rss_module()

    def create_cog(self, reader, channel):
        cog = self.rss_module.RSSFeed.__new__(self.rss_module.RSSFeed)
        cog.reader = reader
        cog.bot = FakeBot(channel)
        return cog

    async def test_check_rss_uses_reader_gemini_and_discord_call_sites(self):
        entry = FakeEntry()
        reader = FakeReader(entry)
        channel = FakeChannel()
        gemini = FakeGeminiClient(
            lambda: types.SimpleNamespace(text="## 測試文章\n翻譯摘要")
        )
        self.rss_module.client = gemini

        await self.rss_module.RSSFeed.check_rss.coro(
            self.create_cog(reader, channel)
        )

        self.assertEqual(reader.update_calls, 1)
        self.assertEqual(len(gemini.models.calls), 1)
        self.assertEqual(
            channel.messages,
            [
                "## <:bun:1445708292142792745> 測試文章\n"
                "翻譯摘要\nhttps://example.com/article"
            ],
        )
        self.assertEqual(reader.marked_entries, [entry])

    async def test_slow_rss_call_site_keeps_heartbeat_responsive(self):
        started = threading.Event()
        release = threading.Event()
        finished = threading.Event()
        heartbeat_count = 0

        def slow_update():
            started.set()
            try:
                release.wait(timeout=1)
            finally:
                finished.set()

        entry = FakeEntry()
        reader = FakeReader(entry, update_feeds=slow_update)
        channel = FakeChannel()
        cog = self.create_cog(reader, channel)
        old_timeout = self.rss_module.EXTERNAL_IO_TIMEOUT
        self.rss_module.EXTERNAL_IO_TIMEOUT = 0.01

        async def heartbeat():
            nonlocal heartbeat_count
            while not finished.is_set():
                heartbeat_count += 1
                await asyncio.sleep(0)

        heartbeat_task = asyncio.create_task(heartbeat())
        try:
            rss_task = asyncio.create_task(self.rss_module.RSSFeed.check_rss.coro(cog))
            self.assertTrue(await asyncio.to_thread(started.wait, 1))
            with self.assertLogs(level=logging.ERROR) as logs:
                await rss_task
            self.assertGreater(heartbeat_count, 0)
            self.assertTrue(any("檢查更新時發生錯誤" in message for message in logs.output))
        finally:
            release.set()
            self.assertTrue(await asyncio.to_thread(finished.wait, 1))
            heartbeat_task.cancel()
            await asyncio.gather(heartbeat_task, return_exceptions=True)
            self.rss_module.EXTERNAL_IO_TIMEOUT = old_timeout

    async def test_slow_gemini_call_site_keeps_heartbeat_responsive(self):
        started = threading.Event()
        release = threading.Event()
        finished = threading.Event()
        heartbeat_count = 0

        def slow_translation():
            started.set()
            try:
                release.wait(timeout=1)
            finally:
                finished.set()
            return types.SimpleNamespace(text="## 測試文章\n翻譯摘要")

        entry = FakeEntry()
        channel = FakeChannel()
        gemini = FakeGeminiClient(slow_translation)
        self.rss_module.client = gemini
        cog = self.create_cog(FakeReader(entry), channel)

        async def heartbeat():
            nonlocal heartbeat_count
            while not finished.is_set():
                heartbeat_count += 1
                await asyncio.sleep(0)

        heartbeat_task = asyncio.create_task(heartbeat())
        send_task = asyncio.create_task(
            cog.send_rss_message(channel, entry, {"emoji": ""})
        )
        try:
            self.assertTrue(await asyncio.to_thread(started.wait, 1))
            await asyncio.sleep(0.01)
            self.assertGreater(heartbeat_count, 0)
            release.set()
            await send_task
            self.assertEqual(len(channel.messages), 1)
        finally:
            release.set()
            await asyncio.to_thread(finished.wait, 1)
            heartbeat_task.cancel()
            await asyncio.gather(heartbeat_task, return_exceptions=True)
            await asyncio.gather(send_task, return_exceptions=True)

    async def test_unavailable_gemini_is_observable_and_wrapped(self):
        entry = FakeEntry()
        channel = FakeChannel()
        gemini = FakeGeminiClient(
            lambda: (_ for _ in ()).throw(OSError("service unavailable"))
        )
        self.rss_module.client = gemini
        cog = self.create_cog(FakeReader(entry), channel)

        with self.assertLogs(level=logging.ERROR) as logs:
            with self.assertRaisesRegex(ExternalIOError, "Gemini translation") as context:
                await cog.send_rss_message(channel, entry, {"emoji": ""})

        self.assertIsInstance(context.exception.__cause__, OSError)
        self.assertEqual(channel.messages, [])
        self.assertTrue(any("Gemini 翻譯失敗" in message for message in logs.output))


if __name__ == "__main__":
    unittest.main()
