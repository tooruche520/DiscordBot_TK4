import asyncio
from datetime import date
import importlib.util
import io
from pathlib import Path
import sqlite3
import sys
import types
import unittest
from unittest.mock import AsyncMock, Mock, patch

import discord
import modules.database


class HappyBirthdayTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        ids = types.ModuleType("modules.database.IdCollectionDatabase")
        ids.get_role_id = lambda name: 1
        ids.get_channel_id = lambda name: 42
        ids.get_emoji_id = lambda name: "ball"
        spec = importlib.util.spec_from_file_location(
            "birthday_under_test",
            Path(__file__).resolve().parents[1] / "cogs/commands/HappyBirthday.py",
        )
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {ids.__name__: ids}):
            with patch("sqlite3.connect", return_value=connection):
                spec.loader.exec_module(self.module)
        self.channel = types.SimpleNamespace(send=AsyncMock())
        self.bot = Mock()
        self.bot.get_channel.return_value = self.channel
        self.bot.get_user.return_value = None
        with patch.object(discord.ext.tasks.Loop, "start"):
            self.cog = self.module.HappyBirthday(self.bot)
        real_file = discord.File
        file_patch = patch.object(
            self.module.discord, "File",
            side_effect=lambda *args, **kwargs: real_file(io.BytesIO(b"image"), **kwargs),
        )
        file_patch.start()
        self.addCleanup(file_patch.stop)
        self.addCleanup(self.cog.check_birthdays_loop.cancel)

    def birthday(self, user_id, year="2000", show_age=1):
        today = date.today()
        self.module.c.execute(
            "INSERT INTO birthdays VALUES (?, ?, ?, ?, ?)",
            (user_id, f"Person {user_id}", year, f"{today.month}-{today.day}", show_age),
        )

    async def test_cache_miss_sends_mentions_for_both_age_settings(self):
        self.birthday(101)
        self.birthday(102, show_age=0)
        await self.cog.check_birthdays_loop()
        calls = self.channel.send.call_args_list
        self.assertEqual(calls[0].args[0], f"祝<@101> {date.today().year - 2000}歲 生日快樂!!")
        self.assertEqual(calls[2].args[0], "祝<@102> 生日快樂!!")
        self.assertEqual(len(calls), 4)
        self.assertNotIn("thumbnail", calls[1].kwargs["embed"].to_dict())

    async def test_cached_user_uses_default_avatar(self):
        self.birthday(101)
        self.bot.get_user.return_value = types.SimpleNamespace(
            mention="<@101>", avatar=None,
            display_avatar=types.SimpleNamespace(url="https://example.com/default.png"),
        )
        await self.cog.check_birthdays_loop()
        embed = self.channel.send.call_args_list[1].kwargs["embed"]
        self.assertEqual(embed.thumbnail.url, "https://example.com/default.png")

    async def test_invalid_record_does_not_block_next_birthday(self):
        self.birthday(101, year="invalid")
        self.birthday(102)
        with self.assertLogs(level="ERROR") as logs:
            await self.cog.check_birthdays_loop()
        self.assertIn("user_id=101", "\n".join(logs.output))
        self.assertIn("channel_id=42", "\n".join(logs.output))
        self.assertIn("<@102>", self.channel.send.call_args_list[0].args[0])

    async def test_send_failure_does_not_block_next_birthday(self):
        for failed_send in (0, 1):
            with self.subTest(failed_send=failed_send):
                self.module.c.execute("DELETE FROM birthdays")
                self.birthday(101)
                self.birthday(102)
                self.channel.send.reset_mock()
                error = discord.HTTPException(
                    types.SimpleNamespace(status=503, reason="Unavailable"), "unavailable",
                )
                self.channel.send.side_effect = [None] * failed_send + [error, None, None]
                with self.assertLogs(level="ERROR"):
                    await self.cog.check_birthdays_loop()
                self.assertIn("<@102>", self.channel.send.call_args_list[-2].args[0])

    async def test_missing_channel_is_reported_and_next_run_recovers(self):
        self.birthday(101)
        self.bot.get_channel.return_value = None
        with self.assertLogs(level="ERROR") as logs:
            await self.cog.check_birthdays_loop()
        self.assertIn("42", "\n".join(logs.output))
        self.channel.send.assert_not_awaited()
        self.bot.get_channel.return_value = self.channel
        await self.cog.check_birthdays_loop()
        self.assertEqual(self.channel.send.await_count, 2)

    async def test_scheduler_survives_failure_and_runs_again(self):
        self.birthday(101)
        delivered = asyncio.Event()
        attempts = 0

        async def send(*args, **kwargs):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise discord.Forbidden(
                    types.SimpleNamespace(status=403, reason="Forbidden"), "forbidden",
                )
            if "embed" in kwargs:
                delivered.set()

        self.channel.send.side_effect = send
        loop = self.cog.check_birthdays_loop

        @loop.before_loop
        async def ready(cog):
            pass

        loop.change_interval(seconds=0.01)
        with self.assertLogs(level="ERROR"):
            task = loop.start()
            try:
                await asyncio.wait_for(delivered.wait(), timeout=1)
                self.assertTrue(loop.is_running())
                self.assertFalse(loop.failed())
            finally:
                loop.cancel()
                await asyncio.gather(task, return_exceptions=True)

    async def test_cancellation_propagates(self):
        self.birthday(101)
        self.bot.get_user.return_value = types.SimpleNamespace(mention="<@101>")
        self.channel.send.side_effect = asyncio.CancelledError()
        with self.assertRaises(asyncio.CancelledError):
            await self.cog.check_birthdays_loop()
