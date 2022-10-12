from discord.ext import commands 
import discord
import json
import logging as log

# logger = log.getLogger()
# logger.setLevel(log.INFO)
# formatter = log.Formatter(fmt='[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# ch = log.StreamHandler()
# ch.setFormatter(formatter)

# log_filename = 'log.txt'
# fh = log.FileHandler(log_filename, encoding='utf-8')
# fh.setFormatter(formatter)

# logger.addHandler(ch)
# logger.addHandler(fh)

class FunnyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open('data.json', "r", encoding = "utf8") as file:
            data = json.load(file)
            self.emoji = data["emoji_list"]

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
    async def 吃(self, ctx, food=""):
        hateFood = ['多益','茄子','青椒']
        loveFood = ['香菜','布丁','咖喱']
        log.info(f'{ctx.author} 打算喂你吃 {food}')
        if (food == ""):
            await ctx.send(f'{ctx.author.mention} 想喂小徹什麽? {self.emoji["tc_tongue"]}')
        elif (food in hateFood):
            await ctx.send(f'小徹拒絕了 {ctx.author.mention} 用 {food} 喂食 {self.emoji["tc_angry"]}')
        elif(food in loveFood):
            await ctx.send(f'小徹接受了 {ctx.author.mention} 用 {food} 喂食 {self.emoji["tc_happy"]}')
        else:
            await ctx.send(f'原來 {ctx.author.mention} 喜歡吃 {food} {self.emoji["tc_is_husky"]}')
            
# 要用 async await 
async def setup(bot):
    await bot.add_cog(FunnyCommands(bot))


# bot 前面記得加 self