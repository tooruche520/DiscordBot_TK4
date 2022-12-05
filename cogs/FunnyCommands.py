from discord.ext import commands 
import discord
import json
import logging as log
import modules.MyDatabase as db
from src.Id_collection import channle_id, emoji_list
from src.greetings_data import morning_response, night_response
from cogs.LevelSystem import LevelSystem
from modules.LimitCounter import add_count

# | 指令       | 描述                    | 經驗值             | 備註                    |
# | ---------- | ----------------------- | ------------------ | ----------------------- |
# | !棒棒糖    | 餵 TK4 一根棒棒糖       | 增加 {N}           |                         |
# | !晚安      | 跟 TK4 說晚安           | 增加 {N}           |                         |
# | !尖頭拉瑞  | 對 TK4 說尖頭拉瑞       | **經驗值不會增加** | 小徹不開心，TK4也不開心 |
# | !吃 \*食物 | 讓 TK4 幫忙送食物給小徹 | 看你給什麼         | 給喜歡的可能會加比較多  |
# | 以下待加入 | ----------------------- | ------------------ | ----------------------- |
# | !rua       | 摸摸TK4 uwu             | 增加 {N}           |                         |

CHANNLE_ID_LEVEL = channle_id["升等通知"]

class FunnyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    @commands.command(brief="餵 TK4 一根棒棒糖", help="增加 10 親密度")
    async def 棒棒糖(self, ctx):
        log.info(f'{ctx.author} 給了TK4一根棒棒糖')
        await ctx.send(f'謝謝 {ctx.author.mention} 的棒棒糖')
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
        # add_count(ctx.author.id)

    # commands
    @commands.command(brief="跟 TK4 說晚安", help="在不同時間會有不同的反應，等你來發掘!")
    async def 晚安(self, ctx):
        log.info(f'{ctx.author} 去睡覺了')
        send_time = ctx.message.create_at()
        # [DEBUG] night_response
        msg = await ctx.send(f'{ctx.author.mention} {night_response(send_time)}')
        msg.add_reaction(emoji_list['tc_tongue']) 
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
        # add_count(ctx.author.id)

    # commands
    @commands.command(brief="對 TK4 說尖頭拉瑞", help="你敢對小徹說尖頭??!?")
    async def 尖頭拉瑞(self, ctx):
        log.info(f'{ctx.author} 叫您尖頭拉瑞')
        await ctx.send(f'對 {ctx.author.mention} 釋放十萬伏特攻擊 -`д´-')
        
    # commands
    @commands.command(brief="", help="")
    async def 小徹(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        await ctx.send(f'{ctx.author.mention} 在攝攝')

    # commands
    @commands.command(brief="摸摸TK4 uwu", help="")
    async def rua(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        await ctx.send(f'{ctx.author.mention} 多...摸摸我一點汪.. {emoji_list["tc_is_husky"]}')
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
        # add_count(ctx.author.id)


    # commands
    @commands.command(brief="跟 TK4 說早安", help="在不同時間會有不同的反應，等你來發掘!")
    async def 早安(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        send_time = ctx.message.create_at()
        # [DEBUG] morning_response
        msg = await ctx.send(f'{ctx.author.mention} {morning_response(send_time)}')
        msg.add_reaction(emoji_list['tc_tongue'])
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
        # add_count(ctx.author.id)


    # commands
    @commands.command(brief="讓 TK4 幫忙送食物給小徹", help="看你給什麼	給喜歡的可能會加比較多親密度")
    async def 吃(self, ctx, food):
        # print(food)
        # food=""
        try:
            hateFood = ['多益','茄子','青椒']
            loveFood = ['香菜','布丁','咖喱']
            log.info(f'{ctx.author} 打算喂你吃 {food}')
            if (food == ""):
                await ctx.send(f'{ctx.author.mention} 想喂小徹什麽? {emoji_list["tc_tongue"]}')
            elif (food in hateFood):
                await ctx.send(f'小徹拒絕了 {ctx.author.mention} 用 {food} 喂食 {emoji_list["tc_angry"]}')
            elif(food in loveFood):
                await ctx.send(f'小徹接受了 {ctx.author.mention} 用 {food} 喂食 {emoji_list["tc_happy"]}')
                await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
            else:
                await ctx.send(f'原來 {ctx.author.mention} 喜歡吃 {food} {emoji_list["tc_is_husky"]}')
        except Exception as e:
            await ctx.send(f'指令錯誤! 請檢查指令之後再次嘗試')
            log.error(f'Error: {e}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        # print(message.content)
        if '<@1028872389385277501>' in message.content:
            await message.channel.send('叫我咪?')
            
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f'指令錯誤! 請檢查指令之後再次嘗試. \n`Error: {error}`')
        
 
            
# 要用 async await 
async def setup(bot):
    await bot.add_cog(FunnyCommands(bot))


# bot 前面記得加 self