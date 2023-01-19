from discord.ext import commands, tasks
import logging as log
import modules.MyDatabase as db
from src.Id_collection import channle_id, emoji_list, role_list
from cogs.LevelSystem import LevelSystem
import modules.CommandsDatabase as command_db
import asyncio

# | 指令       | 描述                    | 經驗值             | 備註                    |
# | ---------- | ----------------------- | ------------------ | ----------------------- |
# | !棒棒糖    | 餵 TK4 一根棒棒糖       | 增加 {N}           |                         |
# | !晚安      | 跟 TK4 說晚安           | 增加 {N}           |                         |
# | !尖頭拉瑞  | 對 TK4 說尖頭拉瑞       | **經驗值不會增加** | 小徹不開心，TK4也不開心 |
# | !吃 \*食物 | 讓 TK4 幫忙送食物給小徹 | 看你給什麼         | 給喜歡的可能會加比較多  |
# | 以下待加入 | ----------------------- | ------------------ | ----------------------- |
# | !rua       | 摸摸TK4 uwu             | 增加 {N}           |                         |

ROLE_HUSKY = role_list["偉大的哈士奇總裁"]

class Test(commands.Cog, description="測試用的類別"):
    def __init__(self, bot):
        self.bot = bot
        
    # [DEBUG] 
    # async def on_ready(self):
    #     # self.bot.bg_task = self.bot.loop.create_loop(self.websocket_task())
    #     @tasks.loop(minutes=5)
    #     async def background_task():
    #         await asyncio.sleep(5)
    #         log.info("Background task is running")
    #     background_task.start()
    # # async def websocket_task(self):
        
        
    # [DEBUG]
    # TODO: 測試沒問題就搬到 FunnyCommands.py
    # async def is_developer(self, ctx):
    #     if(ROLE_HUSKY not in [role.id for role in ctx.author.roles]):
    #         await ctx.send(f"很抱歉，你沒有權限使用此指令\n若你想成為開發者貢獻一份心力，請聯絡小徹")
    #         log.warning(f'{ctx.author} want to use dev command.')
    #         return False
    #     return True
        
    # async def add_my_command(self, name, response, exp):
    #     @commands.command(name=name)
    #     async def fun(ctx):
    #         # log.info(f'{ctx.author} 給了TK4一根棒棒糖')
    #         await ctx.send(response)
    #         await LevelSystem.send_level_up_message(ctx.bot, db.update_user_exp(ctx.author.id, exp), ctx.author)
    #     self.bot.add_command(fun)
    
    # # commands
    # @commands.command(brief="新增臨時自訂指令，現在只有總裁本人能用", help="!add_command [指令名稱] [回覆]")
    # async def add_command(self, ctx, name, response, exp=10):
    #     if self.is_developer(ctx):
    #         await self.add_my_command(name, response, exp)
    #         await ctx.send(f'Add command {name}')
    
    
    # # # [debug]
    # async def add_command_from_database(self, commands_list):
    #     commands_list = command_db.get_all_commands()
    #     for command in commands_list:
    #         name = command[1]
    #         response = command[2]
    #         brief = command[3]
    #         help = command[4]
    #         experience = command[5]
    #         @commands.command(name=name, brief=brief, help=help)
    #         async def fun(ctx):
    #             # log.info(f'{ctx.author} 給了TK4一根棒棒糖')
    #             await ctx.send(response)
    #             # await LevelSystem.send_level_up_message(ctx.bot, db.update_user_exp(ctx.author.id, exp), ctx.author)
    #         self.bot.add_command(fun)
    
    # # [DEBUG]
    # # commands
    # @commands.command()
    # @commands.has_role(ROLE_HUSKY)
    # @commands.guild_only()
    # async def EXP(self, ctx, exp):
    #     await LevelSystem.send_level_up_message(ctx.bot, db.update_user_exp(ctx.author.id, int(exp)), ctx.author)
    #     await ctx.send(f'Add {ctx.author.mention} {exp} exp!')
        
            
    async def on_tweet(self, url):
        await self.get_destination().send("小徹發新照片拉~快去點個讚吧uwu\n"+url)
                
    async def on_tweet_callback(url ,callback):
        callback(url)     
    
    
           
# 要用 async await 
async def setup(bot):
    await bot.add_cog(Test(bot))
