from discord.ext import commands 
import logging as log
import modules.MyDatabase as db
from src.Id_collection import channle_id, emoji_list
from cogs.LevelSystem import LevelSystem

# | 指令       | 描述                    | 經驗值             | 備註                    |
# | ---------- | ----------------------- | ------------------ | ----------------------- |
# | !棒棒糖    | 餵 TK4 一根棒棒糖       | 增加 {N}           |                         |
# | !晚安      | 跟 TK4 說晚安           | 增加 {N}           |                         |
# | !尖頭拉瑞  | 對 TK4 說尖頭拉瑞       | **經驗值不會增加** | 小徹不開心，TK4也不開心 |
# | !吃 \*食物 | 讓 TK4 幫忙送食物給小徹 | 看你給什麼         | 給喜歡的可能會加比較多  |
# | 以下待加入 | ----------------------- | ------------------ | ----------------------- |
# | !rua       | 摸摸TK4 uwu             | 增加 {N}           |                         |

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def add_my_command(self, name, response, exp):
        @commands.command(name=name)
        async def fun(ctx):
            # log.info(f'{ctx.author} 給了TK4一根棒棒糖')
            await ctx.send(response)
            await LevelSystem.send_level_up_message(ctx.bot, db.update_user_exp(ctx.author.id, exp), ctx.author)
        self.bot.add_command(fun)
    
    # commands
    @commands.command()
    async def add_command(self, ctx, name, response):
        await self.add_my_command(name, response, 10)
        await ctx.send(f'Add command {name}')
           
# 要用 async await 
async def setup(bot):
    await bot.add_cog(Test(bot))
