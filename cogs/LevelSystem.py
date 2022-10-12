from discord.ext import commands 
import discord
import json
import logging as log

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
@commands.Cog.listener()
async def on_member_join(member):
    with open('users.json', "r", encoding = "utf8") as f:
        users = json.load(f)
    
    await update_data(users, member)
    
    with open('users.json', "w", encoding = "utf8") as f:
        json.dump(users, f)

@commands.Cog.listener()
async def on_message(message):
    with open('users.json', "r", encoding = "utf8") as f:
        users = json.load(f)
    
    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)
    
    with open('users.json', "w", encoding = "utf8") as f:
        json.dump(users, f)
        
async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** 1/4)
    
    if lvl_start < lvl_end:
        await channel.send(f'{user.mention} 升到了第 {lvl_end}')