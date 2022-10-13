from discord.ext import commands 
import discord
import json
import os
import asyncio
import logging as log

intents=discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

logger = log.getLogger()
logger.setLevel(log.INFO)
formatter = log.Formatter(fmt='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

ch = log.StreamHandler()
ch.setFormatter(formatter)

log_filename = 'log.txt'
fh = log.FileHandler(log_filename, encoding='utf-8')
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

with open('token.json', "r", encoding = "utf8") as file:
    data = json.load(file)
    token = data['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print("Bot in ready")
    log.info("Bot in ready")

@bot.command()
async def reload(ctx, extension):
    log.info(f"reloading {extension}")
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"reloaded {extension}")

@bot.command()
async def reload_all(ctx):
    print(f"reloading all extensions...")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.reload_extension(f"cogs.{filename[:-3]}")
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
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())

bot.run(token) 
