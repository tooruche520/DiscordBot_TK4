from discord.ext import commands, tasks
import logging as log
import modules.database.UserDatabase as db
import modules.database.IdCollectionDatabase as ID
from cogs.LevelSystem import LevelSystem
import modules.database.CommandsDatabase as command_db
import asyncio


ROLE_HUSKY = ID.get_role_id("偉大的哈士奇總裁")

class Test(commands.Cog, description="測試用的類別"):
    def __init__(self, bot):
        self.bot = bot
    
           
# 要用 async await 
async def setup(bot):
    await bot.add_cog(Test(bot))
