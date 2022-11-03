from discord.ext import commands 
import discord
import json
import logging as log
from src.Id_collection import channle_id

CHANNLE_ID_LEVEL = channle_id["等級測試"]

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_data(self, users, user):
        user_id = str(user.id)
        # print(user.id)
        # print(users)
        # print(str(user.id) in users)
        if not str(user.id) in users:
            users[user_id] = {}
            users[user_id]['experience'] = 0
            users[user_id]['level'] = 1
            log.info(f'加入使用者{user}')

    async def add_experience(self, users, user, exp):
        user_id = str(user.id)
        users[user_id]['experience'] += exp
        log.info(f'增加 {user} {exp} 經驗值')

    async def level_up(self, users, user, channel):
        user_id = str(user.id)
        experience = users[user_id]['experience']
        lvl_start = users[user_id]['level']
        lvl_end = int(experience ** (1/4))
        
        if lvl_start < lvl_end:
            users[user_id]['level'] = lvl_end
            log.info(f'{user.mention} 升到了第{lvl_end}等')
            await channel.send(f'{user.mention} 升到了第{lvl_end}等')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('users.json', "r", encoding = "utf8") as f:
            users = json.load(f)
            log.info("讀入users.json")
        
        await self.update_data(users, member)
        
        with open('users.json', "w", encoding = "utf8") as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        with open('users.json', "r", encoding = "utf8") as f:
            users = json.load(f)
        
        channel = self.bot.get_channel(CHANNLE_ID_LEVEL)
        await self.update_data(users, message.author)
        await self.add_experience(users, message.author, 5)
        await self.level_up(users, message.author, channel)
        
        with open('users.json', "w", encoding = "utf8") as f:
            json.dump(users, f)


    @commands.command()
    async def level(self, ctx):
        try:
            with open('users.json', "r", encoding = "utf8") as f:
                users = json.load(f)
                user_id = str(ctx.author.id) 
                experience = users[user_id]['experience']
                level = users[user_id]['level']
                await ctx.send(f'{ctx.author.mention} 目前是等級{level}，累積了{experience}經驗值!!')
        except Exception as e:
            log.info("Error loading users.json") 

# 要用 async await 
async def setup(bot):
    await bot.add_cog(LevelSystem(bot))
