from discord.ext import commands 
from discord.user import User
import os
import logging as log
from src.Id_collection import role_list, emoji_list
import modules.MyDatabase as db

ROLE_DEVELOPER = role_list["TK4開發團隊"]

class DebugCommand(commands.Cog, description="TK4開發專用除錯指令，只有TK4開發團隊有權限使用"):
    def __init__(self, bot):
        self.bot = bot

    async def is_developer(self, ctx):
        if isinstance(ctx.author, User):
            await ctx.send(f"你正在私人頻道中，無法使用指令")
            return False

        if(ROLE_DEVELOPER not in [role.id for role in ctx.author.roles]):
            await ctx.send(f"很抱歉，你沒有權限使用此指令\n若你想成為開發者貢獻一份心力，請聯絡小徹")
            log.warning(f'{ctx.author} want to use dev command.')
            return False
        return True
        

    # Reload one Cog you specified. 
    @commands.command(brief="重新讀取指定cog", help="!reload [指定cog名稱]")
    # @commands.has_role(ROLE_DEVELOPER)
    async def reload(self, ctx, extension):
        if(not await self.is_developer(ctx)):
            return

        await self.bot.reload_extension(f"cogs.{extension}")
        log.info(f"Completed reloading {extension}")
        await ctx.send(f"reloaded {extension}")

    # Reload all Cog in project. 
    @commands.command(brief="重新讀取所有cog", help="!reload_all")
    async def reload_all(self, ctx):
        if(not await self.is_developer(ctx)):
            return
        
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[:-3]}")
        log.info(f"Completed reloading all extensions.")
        await ctx.send(f"reloaded all")

    # Delete the last {limit} messages.
    @commands.command(brief="刪除當前頻道的指定數量訊息", help="!delete_all [訊息數量]")
    async def delete_all(self, ctx, limit):
        if(not await self.is_developer(ctx)):
            return

        async for message in ctx.channel.history(limit=int(limit)):
            await message.delete()
            # log.info(f"deleted message {message.content}")
        log.info(f"completed deleted {limit} messages")

    # Shutdown bot by command.
    @commands.command(brief="讓TK4休息一下", help="!shutdown")
    async def shutdown(self, ctx):
        if(not await self.is_developer(ctx)):
            return
        await ctx.send(f'休息時間到了咪~\n等等見囉{emoji_list["tc_tongue"]}')
        log.info(f'Bot ended: command')
        await self.bot.close()
        
    
    @commands.command(brief="重新整理使用者等級與親密度", help="!reload_user_exp")
    async def reload_user_exp(self, ctx):
        for guild in self.bot.guilds:
            for member in guild.members:
                db.reload_user_exp(member.id)
        log.info(f'Susseccfully reloaded user exp and level from csv.')


# 要用 async await 
async def setup(bot):
    await bot.add_cog(DebugCommand(bot))

# bot 前面記得加 self
