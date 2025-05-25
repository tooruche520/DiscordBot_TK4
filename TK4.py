from discord.ext import tasks, commands
import discord
import os
import asyncio
import time
import logging as log
from modules.TK4_Logger import TK4_logger
from dotenv import dotenv_values
from modules.CustomHelpCommand import CustomHelpCommand
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=CustomHelpCommand())

TK4_logger()
config = dotenv_values(".env")
DISCORD_BOT_TOKEN = config.get("DISCORD_BOT_TOKEN")

@bot.event
async def on_ready():
    log.info("Bot in ready")     

async def load_extensions(bot):
    async def load_extension_from_path(path):
        for root, _, files in os.walk(path):
            # Skip deprecated directory
            if 'deprecated' in root:
                continue
            for filename in files:
                if filename.endswith('.py'):
                    ext_path = os.path.relpath(os.path.join(root, filename), path).replace(os.sep, '.')[:-3]
                    try:
                        await bot.load_extension(f'cogs.{ext_path}')
                    except Exception as e:
                        log.error(f'Failed to load extension cogs.{ext_path}\n{e}')
    try:
        await load_extension_from_path("./cogs")
    except Exception as e:
        log.error(e)

async def main():
    async with bot:
        await load_extensions(bot)
        await bot.start(DISCORD_BOT_TOKEN)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    log.error(f'Bot ended: KeyboardInterrupt')
except Exception as e:
    log.error(f'Bot ended: {e}')


