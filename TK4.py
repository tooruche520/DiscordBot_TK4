from discord.ext import tasks, commands
import discord
import json
import os
import asyncio
import time
from modules.TK4_Logger import TK4_logger
import logging as log
from dotenv import dotenv_values


intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

TK4_logger()
config = dotenv_values(".env")
DISCORD_BOT_TOKEN = config.get("DISCORD_BOT_TOKEN")

@bot.event
async def on_ready():
    log.info("Bot in ready")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    log.info(f"Completed reloading {extension}")
    await ctx.send(f"reloaded {extension}")

@bot.command()
async def reload_all(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.reload_extension(f"cogs.{filename[:-3]}")
    log.info(f"Completed reloading all extensions.")
    await ctx.send(f"reloaded all")
    # await bot.reload_extension(f"cogs.{extension}")

# 臨時用
# @bot.command()
# async def delete(ctx, limit):
#     async for message in ctx.channel.history(limit=int(limit)):
#         if message.author == bot.user and '升到了第' in message.content:
#             await message.delete()
#             log.info(f"deleted message {message.content}")
#         else:
#             log.info(f"no delete message {message.content}")
#     log.info(f"completed deleted message")
        

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


