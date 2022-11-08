from discord.ext import commands 
from discord.abc import User
import os
import logging as log
from src.Id_collection import role_list

ROLE_DEVELOPER = role_list["TK4開發團隊"]

class DebugCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_developer(self, ctx):
        if isinstance(ctx.author, User):
            await ctx.send(f"You are in the private channel.")
            return False

        if(ROLE_DEVELOPER not in [role.id for role in ctx.author.roles]):
            await ctx.send(f"You don't have permission use this command.")
            log.warning(f'{ctx.author} want to use dev command.')
            return False
        return True

    # Reload one Cog you specified. 
    @commands.command()
    async def reload(self, ctx, extension):
        if(not await self.is_developer(ctx)):
            return

        await self.bot.reload_extension(f"cogs.{extension}")
        log.info(f"Completed reloading {extension}")
        await ctx.send(f"reloaded {extension}")

    # Reload all Cog in project. 
    @commands.command()
    async def reload_all(self, ctx):
        if(not await self.is_developer(ctx)):
            return
        
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.bot.reload_extension(f"cogs.{filename[:-3]}")
        log.info(f"Completed reloading all extensions.")
        await ctx.send(f"reloaded all")

    # Delete the last {limit} messages.
    @commands.command()
    async def delete_all(self, ctx, limit):
        if(not await self.is_developer(ctx)):
            return

        async for message in ctx.channel.history(limit=int(limit)):
            await message.delete()
            # log.info(f"deleted message {message.content}")
        log.info(f"completed deleted {limit} messages")

    # Shutdown bot by command.
    @commands.command()
    async def shutdown(self, ctx):
        if(not await self.is_developer(ctx)):
            return
        log.info(f'Bot ended: command')
        await self.bot.close()
        


# 要用 async await 
async def setup(bot):
    await bot.add_cog(DebugCommand(bot))

# bot 前面記得加 self
