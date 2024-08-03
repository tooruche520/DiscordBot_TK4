from discord.ext import commands 
import discord
import os
import logging as log
from src.Id_collection import role_list, emoji_list
import modules.database.UserDatabase as db
import modules.database.CommandsDatabase as command_db
from cogs.LevelSystem import LevelSystem

ROLE_DEVELOPER = role_list["TK4開發團隊"]
ROLE_HUSKY = role_list["偉大的哈士奇總裁"]

class DebugCommand(commands.Cog, description="TK4開發專用除錯指令，只有TK4開發團隊有權限使用"):
    def __init__(self, bot):
        self.bot = bot


        

    # Reload one Cog you specified. 
    @commands.command(brief="重新讀取指定cog", help="!reload [指定cog名稱]")
    @commands.has_role(ROLE_DEVELOPER)
    async def reload(self, ctx, extension):
        for root, _, files in os.walk("./cogs"):
            # Skip deprecated directory
            if 'deprecated' in root:
                continue
            for filename in files:
                if filename == f"{extension}.py":
                    ext_path = os.path.relpath(os.path.join(root, filename), "./cogs").replace(os.sep, '.')[:-3]
                                        
                    try:
                        await self.bot.reload_extension(f'cogs.{ext_path}')
                        log.info(f"Completed reloading {extension}")
                        await ctx.send(f"reloaded {extension}")
                        return
                    except Exception as e:
                        log.error(f"Failed to reload extension cogs.{ext_path}\n{e}")
                        await ctx.send(f"Failed to reloaded {extension}")
                        
        log.error(f"Failed to reload {extension}. No extension found.")
        await ctx.send(f"Failed to reload {extension}. No extension found.")
                

    # Reload all Cog in project. 
    @commands.command(brief="重新讀取所有cog", help="!reload_all")
    @commands.has_role(ROLE_DEVELOPER)
    async def reload_all(self, ctx):
        for root, _, files in os.walk("./cogs"):
            # Skip deprecated directory
            if 'deprecated' in root:
                continue
            for filename in files:
                if filename.endswith('.py'):
                    ext_path = os.path.relpath(os.path.join(root, filename), "./cogs").replace(os.sep, '.')[:-3]
                    try:
                        await self.bot.reload_extension(f'cogs.{ext_path}')
                    except Exception as e:
                        log.error(f'Failed to load extension cogs.{ext_path}\n{e}')
        log.info(f"Completed reloading all extensions.")
        await ctx.send(f"reloaded all")

    # Delete the last {limit} messages.
    @commands.command(brief="刪除當前頻道的指定數量訊息", help="!delete_all [訊息數量]")
    @commands.has_role(ROLE_DEVELOPER)
    async def delete_all(self, ctx, limit):
        async for message in ctx.channel.history(limit=int(limit)):
            await message.delete()
            # log.info(f"deleted message {message.content}")
        log.info(f"completed deleted {limit} messages")

    # Shutdown bot by command.
    @commands.command(brief="讓TK4休息一下", help="!關機睡覺")
    @commands.has_role(ROLE_DEVELOPER)
    async def 關機睡覺(self, ctx):
        await ctx.send(f'休息時間到了咪~\n等等見囉{emoji_list[":tc_tongue:"]}')
        log.info(f'Bot ended: command')
        await self.bot.close()
        

    @commands.command()
    @commands.has_role(ROLE_HUSKY)
    @commands.guild_only()
    async def EXP(self, ctx, exp):
        await LevelSystem.send_level_up_message(ctx.bot, db.update_user_exp(ctx.author.id, int(exp)), ctx.author)
        await ctx.send(f'Add {ctx.author.mention} {exp} exp!')
        
        
    @commands.command(brief="產生每月指令使用量結算表", help="!每月結算 [月份] [平台名稱]\n月份格式：2023-02\n平台格式：discord / twitch")
    @commands.has_role(ROLE_HUSKY)
    async def 每月結算(self, ctx, month_format, platform):
        command_db.make_csv(month_format, platform)
        await ctx.send(file=discord.File(f'每月指令統計表({platform}).csv'))
    # @commands.command()
    # async def reload_user_exp(self, ctx):
    #     for guild in self.bot.guilds:
    #         for member in guild.members:
    #             db.reload_user_exp(member.id)
    #     log.info(f'Susseccfully reloaded user exp and level from csv.')


# 要用 async await 
async def setup(bot):
    await bot.add_cog(DebugCommand(bot))

# bot 前面記得加 self
