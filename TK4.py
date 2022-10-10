from discord.ext import commands 
import discord
import json

intents=discord.Intents.all()

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

with open('token.json', "r", encoding = "utf8") as file:
    data = json.load(file)


@bot.event
async def on_ready():
    print("Bot in ready")

@bot.event
async def on_member_join(member):
    print(f'{member} join')
    channel = bot.get_channel(1028290028721406013)
    await channel.send(f'{member} join')

    
bot.run(data['token']) 