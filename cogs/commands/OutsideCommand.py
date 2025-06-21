from discord.ext import commands 
import logging as log
import modules.database.UserDatabase as db
from cogs.LevelSystem import LevelSystem

class OutsideCommand(commands.Cog, description="外部程式建立的指令，這邊會進行集中管理"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='天氣', brief='透過AI幫你分析今日天氣!', help="!天氣 [頻道ID] [文字訊息]")
    async def func(self, ctx, message):
        exp = 5
        log.info(f'{ctx.author} 發送了天氣指令: {message}')
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, exp), ctx.author)


# 要用 async await 
async def setup(bot):
    await bot.add_cog(OutsideCommand(bot))

# bot 前面記得加 self
