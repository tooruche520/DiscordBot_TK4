from discord.ext import commands 
from discord.user import User
import os
import logging as log
from src.Id_collection import role_list, emoji_list
import modules.MyDatabase as db

ROLE_DEVELOPER = role_list["TK4開發團隊"]

class HappyBirthday(commands.Cog, description="TK4祝尼生日快樂uwu"):
    def __init__(self, bot):
        self.bot = bot

    # Shutdown bot by command.
    @commands.command(brief="讓TK4休息一下", help="!shutdown")
    @commands.has_role(ROLE_DEVELOPER)
    async def 生日(self, ctx, date):
        await ctx.send(f'休息時間到了咪~\n等等見囉{emoji_list["tc_tongue"]}')
        log.info(f'Bot ended: command')
        await self.bot.close()

# 要用 async await 
async def setup(bot):
    await bot.add_cog(HappyBirthday(bot))

# bot 前面記得加 self
