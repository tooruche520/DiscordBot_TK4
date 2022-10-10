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
    token = data['token']

@bot.event
async def on_ready():
    print("Bot in ready")


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
