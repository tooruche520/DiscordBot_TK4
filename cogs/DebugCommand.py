from discord.ext import commands 
import os
import logging as log
from src.Id_collection import role_list

ROLE_DEVELOPER = role_list["TK4開發團隊"]

class DebugCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_developer(self, ctx):
        # print(ctx.author.roles, ROLE_DEVELOPER)
        # print([role for role in ctx.author.roles])
        return ROLE_DEVELOPER in [role.id for role in ctx.author.roles]

    # commands
    @commands.command()
    async def reload(self, ctx, extension):
        if(not self.is_developer(ctx)):
            await ctx.send(f"You don't have permission use this command.")
            return

        await self.bot.reload_extension(f"cogs.{extension}")
        log.info(f"Completed reloading {extension}")
        await ctx.send(f"reloaded {extension}")

    @commands.command()
    async def reload_all(self, ctx):
        if(not self.is_developer(ctx)):
            await ctx.send(f"You don't have permission use this command.")
            return
        
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[:-3]}")
        log.info(f"Completed reloading all extensions.")
        await ctx.send(f"reloaded all")



# 要用 async await 
async def setup(bot):
    await bot.add_cog(DebugCommand(bot))

# bot 前面記得加 self
