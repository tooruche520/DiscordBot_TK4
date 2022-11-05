from discord.ext import commands 
import discord
import json
import logging as log
from src.Id_collection import channle_id
import modules.MyDatabase as db
# import modules.User as User
from modules.User import User

CHANNLE_ID_LEVEL = channle_id["等級測試"]

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_level_up_message(self, is_upgrade, user):
        if(is_upgrade):
            channel = self.bot.get_channel(CHANNLE_ID_LEVEL)
            user_data = db.get_user_by_userid(user.id)
            level = user_data.level
            await channel.send(f'{user.mention} 升到了第{level}等')
        return

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                db.add_user(User(member.id))
        log.info(f"Successfully add all user from Server")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        user_id = member.id
        user_adoption = User.Adoption.VIP
        db.add_user(User(user_id, user_adoption))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
            
        if message.content[0] == '!':
            return

        await self.send_level_up_message(db.update_user_exp(message.author.id, 2), message.author)
        

    @commands.command()
    async def level(self, ctx):
        user_data = db.get_user_by_userid(ctx.author.id)
        level = user_data.level
        experience = user_data.experience
        await ctx.send(f'{ctx.author.mention} 目前是等級{level}，累積了{experience}經驗值!!')


# 要用 async await 
async def setup(bot):
    await bot.add_cog(LevelSystem(bot))

