from discord.ext import commands 
import discord
import json
import logging as log
import modules.MyDatabase as db
from src.Id_collection import channle_id, emoji_list, role_list
from src.greetings_data import morning_response, night_response
from cogs.LevelSystem import LevelSystem
import modules.CommandsDatabase as command_db


# | 指令       | 描述                    | 經驗值             | 備註                    |
# | ---------- | ----------------------- | ------------------ | ----------------------- |
# | !棒棒糖    | 餵 TK4 一根棒棒糖       | 增加 {N}           |                         |
# | !晚安      | 跟 TK4 說晚安           | 增加 {N}           |                         |
# | !尖頭拉瑞  | 對 TK4 說尖頭拉瑞       | **經驗值不會增加** | 小徹不開心，TK4也不開心 |
# | !吃 \*食物 | 讓 TK4 幫忙送食物給小徹 | 看你給什麼         | 給喜歡的可能會加比較多  |
# | 以下待加入 | ----------------------- | ------------------ | ----------------------- |
# | !rua       | 摸摸TK4 uwu             | 增加 {N}           |                         |

CHANNLE_ID_LEVEL = channle_id["升等通知"]
ROLE_HUSKY = role_list["偉大的哈士奇總裁"]

class FunnyCommands(commands.Cog, description="你可以用這些指令與TK4對話"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.add_command_from_database()

    # commands
    @commands.command(brief="餵 TK4 一根棒棒糖", help="!棒棒糖\n可以增加 10 親密度")
    async def 棒棒糖(self, ctx):
        log.info(f'{ctx.author} 給了TK4一根棒棒糖')
        await ctx.send(f'謝謝 {ctx.author.mention} 的棒棒糖')
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
        # [DEBUG]
        command_db.update_counter(ctx.command.name, ctx.message.created_at)

    # commands
    @commands.command(brief="跟 TK4 說早安", help="!早安\n在不同時間會有不同的反應，等你來發掘!")
    async def 早安(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        send_time = ctx.message.created_at
        msg = await ctx.send(f'{ctx.author.mention} {morning_response(send_time)}')
        await msg.add_reaction(emoji_list['tc_tongue'])
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
        # add_count(ctx.author.id)

    # commands
    @commands.command(brief="跟 TK4 說晚安", help="!晚安\n在不同時間會有不同的反應，等你來發掘!")
    async def 晚安(self, ctx):
        log.info(f'{ctx.author} 去睡覺了')
        send_time = ctx.message.created_at
        msg = await ctx.send(f'{ctx.author.mention} {night_response(send_time)}')
        await msg.add_reaction(emoji_list['tc_tongue']) 
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
        # add_count(ctx.author.id)

    # commands
    @commands.command(brief="對小徹說尖頭拉瑞", help="你敢對小徹說尖頭??!?")
    async def 尖頭拉瑞(self, ctx):
        log.info(f'{ctx.author} 叫您尖頭拉瑞')
        await ctx.send(f'對 {ctx.author.mention} 釋放十萬伏特攻擊 -`д´-')
        
    # commands
    @commands.command(brief="叫一下小徹", help="!小徹\n這並不會幫你@小徹 有事請直接使用tag讓我看到")
    async def 小徹(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        await ctx.send(f'{ctx.author.mention} 他在攝攝，有事請直接@小徹')

    # commands
    @commands.command(brief="摸摸TK4 uwu", help="!rua\n每日療癒")
    async def rua(self, ctx):
        log.info(f'{ctx.author} 在叫你')
        await ctx.send(f'{ctx.author.mention} 多...摸摸我一點汪.. {emoji_list["tc_is_husky"]}')
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, 10), ctx.author)
        # add_count(ctx.author.id)


    # commands
    @commands.command(brief="讓 TK4 幫忙送食物給小徹", help="!吃 [給小徹吃的東西]\n看你給什麼 給喜歡的可能會加比較多親密度")
    async def 吃(self, ctx, food):
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
            await ctx.send(f'AAA')
            log.error(f'Error: {e}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        # print(message.content)
        if '<@1028872389385277501>' in message.content:
            await message.channel.send('叫我咪?')
            
            
    async def add_my_command(self, name, response, exp):
        @commands.command(name=name)
        async def fun(ctx):
            await ctx.send(response)
            await LevelSystem.send_level_up_message(ctx.bot, db.update_user_exp(ctx.author.id, exp), ctx.author)
        self.bot.add_command(fun)
    
    
    # commands
    @commands.has_role(ROLE_HUSKY)
    @commands.guild_only()
    @commands.command(brief="新增臨時自訂指令，現在只有總裁本人能用", help="!add_command [指令名稱] [回覆]")
    async def add_command(self, ctx, name, response, exp=10):
        await self.add_my_command(name, response, exp)
        await ctx.send(f'Add command {name}')
        print(self.add_command.cog_name)
    
    
    # [DEBUG]
    async def add_command_from_database(self):
        commands_list = command_db.get_all_commands()
        for command in commands_list:
            name = command[1]
            response = command[2]
            brief = command[3]
            help = command[4]
            experience = command[5]
            @commands.command(name=name, brief=brief, help=help)
            async def fun(ctx):
                # log.info(f'{ctx.author} 給了TK4一根棒棒糖')
                await ctx.send(response)
                # await LevelSystem.send_level_up_message(ctx.bot, db.update_user_exp(ctx.author.id, exp), ctx.author)
            self.bot.add_command(fun)
    
    # [DEBUG]
    # commands
    @commands.command()
    @commands.has_role(ROLE_HUSKY)
    @commands.guild_only()
    async def EXP(self, ctx, exp):
        await LevelSystem.send_level_up_message(ctx.bot, db.update_user_exp(ctx.author.id, int(exp)), ctx.author)
        await ctx.send(f'Add {ctx.author.mention} {exp} exp!')
            
# 要用 async await 
async def setup(bot):
    await bot.add_cog(FunnyCommands(bot))


# bot 前面記得加 self