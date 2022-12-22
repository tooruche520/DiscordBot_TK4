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

async def load_extensions():
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
    except Exception as e:
        log.error(e)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_BOT_TOKEN)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    log.error(f'Bot ended: KeyboardInterrupt')
except Exception as e:
    log.error(f'Bot ended: {e.message}')


