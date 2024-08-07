from discord.ext import commands 
import discord
import os
import logging as log
import modules.database.IdCollectionDatabase as ID
import modules.database.UserDatabase as db
import modules.database.CommandsDatabase as command_db
from cogs.LevelSystem import LevelSystem

ROLE_DEVELOPER = ID.get_role_id("TK4開發團隊")
ROLE_HUSKY = ID.get_role_id("偉大的哈士奇總裁")

class SendMessage(commands.Cog, description="TK4開發專用除錯指令，只有TK4開發團隊有權限使用"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='send', brief='發送訊息至指定頻道', help="!send [頻道ID] [文字訊息]")
    @commands.has_role(ROLE_HUSKY)
    @commands.guild_only()
    async def send_message(self, ctx, channel: discord.TextChannel, message):
    
        # 發送訊息到指定頻道
        await channel.send(message)
        await ctx.send(f'已成功發送訊息至 <#{channel.id}>。')

    


# 要用 async await 
async def setup(bot):
    await bot.add_cog(SendMessage(bot))

# bot 前面記得加 self
