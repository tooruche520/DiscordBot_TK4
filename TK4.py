from discord.ext import commands 
import discord
import json

intents=discord.Intents.all()

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

with open('token.json', "r", encoding = "utf8") as file:
    data = json.load(file)
    token = data['token']

with open('data.json', "r", encoding = "utf8") as file:
    data = json.load(file)

@bot.event
async def on_ready():
    print("Bot in ready")

@bot.event
async def on_member_join(member):
    print(f'{member} join')
    channel = bot.get_channel(int(data["TK4開發測試頻道"]))
    await channel.send(f'{member.mention} join')

@bot.event
async def on_member_remove(member):
    print(f'{member} leave')
    channel = bot.get_channel(int(data["TK4開發測試頻道"]))
    await channel.send(f'{member.mention} leave')

@bot.command()
async def 棒棒糖(ctx):
    print(f'{ctx.author}給了TK4一根棒棒糖')
    await ctx.send(f'謝謝{ctx.author.mention}的棒棒糖')

    
bot.run(token) 