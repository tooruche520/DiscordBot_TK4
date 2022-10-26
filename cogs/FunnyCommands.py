from discord.ext import commands 
import discord
import json
import logging as log
from src.Id_collection import channle_id, emoji_list

# | 指令       | 描述                    | 經驗值             | 備註                    |
# | ---------- | ----------------------- | ------------------ | ----------------------- |
# | !棒棒糖    | 餵 TK4 一根棒棒糖       | 增加 {N}           |                         |
# | !晚安      | 跟 TK4 說晚安           | 增加 {N}           |                         |
# | !尖頭拉瑞  | 對 TK4 說尖頭拉瑞       | **經驗值不會增加** | 小徹不開心，TK4也不開心 |
# | !吃 \*食物 | 讓 TK4 幫忙送食物給小徹 | 看你給什麼         | 給喜歡的可能會加比較多  |
# | 以下待加入 | ----------------------- | ------------------ | ----------------------- |
# | !rua       | 摸摸TK4 uwu             | 增加 {N}           |                         |

class FunnyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    @commands.command()
    async def 棒棒糖(self, ctx):
        log.info(f'{ctx.author} 給了TK4一根棒棒糖')
        await ctx.send(f'謝謝 {ctx.author.mention} 的棒棒糖')

    # commands
    @commands.command()
    async def 晚安(self, ctx):
        log.info(f'{ctx.author} 去睡覺了')
        await ctx.send(f'{ctx.author.mention} 晚安晚安汪(*´∀`)~♥')

    # commands
    @commands.command()
    async def 尖頭拉瑞(self, ctx):
        log.info(f'{ctx.author} 叫您尖頭拉瑞')
        await ctx.send(f'對 {ctx.author.mention} 釋放十萬伏特攻擊 -`д´-')
        
    # commands
    @commands.command()
    async def 小徹(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        await ctx.send(f'{ctx.author.mention} 在攝攝')

    # commands
    @commands.command()
    async def rua(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        await ctx.send(f'{ctx.author.mention} 多...摸摸我一點汪.. {emoji_list["tc_is_husky"]}')

    # commands
    @commands.command()
    async def 早安(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        await ctx.send(f'{ctx.author.mention} 早安早安汪 {emoji_list["tc_is_husky"]}')


    # commands
    @commands.command()
    async def 吃(self, ctx, food=""):
        hateFood = ['多益','茄子','青椒']
        loveFood = ['香菜','布丁','咖喱']
        log.info(f'{ctx.author} 打算喂你吃 {food}')
        if (food == ""):
            await ctx.send(f'{ctx.author.mention} 想喂小徹什麽? {emoji_list["tc_tongue"]}')
        elif (food in hateFood):
            await ctx.send(f'小徹拒絕了 {ctx.author.mention} 用 {food} 喂食 {emoji_list["tc_angry"]}')
        elif(food in loveFood):
            await ctx.send(f'小徹接受了 {ctx.author.mention} 用 {food} 喂食 {emoji_list["tc_happy"]}')
        else:
            await ctx.send(f'原來 {ctx.author.mention} 喜歡吃 {food} {emoji_list["tc_is_husky"]}')
            
# 要用 async await 
async def setup(bot):
    await bot.add_cog(FunnyCommands(bot))


# bot 前面記得加 self