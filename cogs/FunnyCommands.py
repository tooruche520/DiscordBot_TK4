from email import message
from http import client
from multiprocessing.connection import Client
from discord.ext import commands 
import discord


class FunnyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    @commands.command()
    async def 棒棒糖(self, ctx):
        print(f'{ctx.author} 給了TK4一根棒棒糖')
        await ctx.send(f'謝謝 {ctx.author.mention} 的棒棒糖')

    # commands
    @commands.command()
    async def 晚安(self, ctx):
        print(f'{ctx.author} 去睡覺了')
        await ctx.send(f'{ctx.author.mention} 晚安晚安汪(*´∀`)~♥')
        
    # commands
    @commands.command()
    async def 尖頭拉瑞(self, ctx):
        print(f'{ctx.author} 叫您尖頭拉瑞')
        await ctx.send(f'對 {ctx.author.mention} 釋放十萬伏特攻擊 -`д´-')
        
    # commands
    @commands.command()
    async def 小徹(self, ctx):
        print(f'{ctx.author} 在叫你')
        await ctx.send(f'{ctx.author.mention} 在攝攝')
        
    # commands
    @commands.command()
    async def 吃(self, ctx, food=""):
        hateFood = ['多益','茄子','青椒']
        loveFood = ['香菜','布丁','咖喱']
        print(f'{ctx.author} 打算喂你吃 {food}')
        if (food == ""):
            await ctx.send(f'{ctx.author.mention} 想喂小徹什麽? :tc_tongue:')
        elif (food in hateFood):
            await ctx.send(f'小徹拒絕了 {ctx.author.mention} 用 {food} 喂食 :tc_angry:')
        elif(food in loveFood):
            await ctx.send(f'小徹接受了 {ctx.author.mention} 用 {food} 喂食 :tc_happy:')
        else:
            await ctx.send(f'原來 {ctx.author.mention} 喜歡吃 {food} :tc_is_husky:')
            

# 要用 async await 
async def setup(bot):
    await bot.add_cog(FunnyCommands(bot))


# bot 前面記得加 self