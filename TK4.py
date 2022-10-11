from discord.ext import commands 
import discord
import json
import os
import asyncio

intents=discord.Intents.all()

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

with open('token.json', "r", encoding = "utf8") as file:
    data = json.load(file)
    token = data['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print("Bot in ready")

@bot.command()
async def reload(ctx, extension):
    print(f"reloading {extension}")
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
