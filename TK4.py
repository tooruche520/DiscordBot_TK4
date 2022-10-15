from discord.ext import tasks, commands
import discord
import json
import os
import asyncio
import logging as log
import time

log_dir = os.getcwd() + '\\LogFiles\\'
log_path = os.getcwd() + os.sep + log_dir
os.makedirs(log_dir)

intents=discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

logger = log.getLogger()
logger.setLevel(log.INFO)
formatter = log.Formatter(fmt='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S',)

ch = log.StreamHandler()
ch.setFormatter(formatter)

log_filename = log_dir + time.strftime("%Y-%m-%d") + ' log .txt'
fh = log.FileHandler(log_filename, encoding='utf-8',)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

with open('token.json', "r", encoding = "utf8") as file:
    data = json.load(file)
    token = data['DISCORD_BOT_TOKEN']

def LogFolder(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        log.info(f'Create Folder "LogFiles" ')
    else:
        log.info(f'The Folder "LogFiles" are already have')

@bot.event
async def on_ready():
    log.info("Bot in ready")
    LogFolder(log_dir)

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
        await bot.start(token)

try:
    asyncio.run(main())
except Exception as e:
    log.error(f'Bot ended: {e.message}')


