from discord.ext import commands 
import logging as log
import re
import modules.database.UserDatabase as db
import modules.database.CommandsDatabase as command_db
import modules.database.IdCollectionDatabase as ID
from modules.database.ResponseDatabase import get_greeting_response
from cogs.LevelSystem import LevelSystem
from modules.EmojiReplace import replace_emoji_dc
from cogs.ExtraExp import get_extra_exp


# | 指令       | 描述                    | 經驗值             | 備註                    |
# | ---------- | ----------------------- | ------------------ | ----------------------- |
# | !棒棒糖    | 餵 TK4 一根棒棒糖       | 增加 {N}           |                         |
# | !晚安      | 跟 TK4 說晚安           | 增加 {N}           |                         |
# | !尖頭拉瑞  | 對 TK4 說尖頭拉瑞       | **經驗值不會增加** | 小徹不開心，TK4也不開心 |
# | !吃 \*食物 | 讓 TK4 幫忙送食物給小徹 | 看你給什麼         | 給喜歡的可能會加比較多  |
# | 以下待加入 | ----------------------- | ------------------ | ----------------------- |
# | !rua       | 摸摸TK4 uwu             | 增加 {N}           |                         |

CHANNEL_ID_LEVEL = ID.get_channel_id("升等通知")
ROLE_HUSKY = ID.get_role_id("偉大的哈士奇總裁")
command_reply_dict = command_db.get_reply()

class FunnyCommands(commands.Cog, description="你可以用這些指令與TK4對話"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.add_command_from_database()

         
    @commands.command(brief="跟 TK4 說早安", help="!早安\n在不同時間會有不同的反應，等你來發掘!")
    async def 早安(self, ctx):
        exp = 10
        log.info(f'{ctx.author} 在叫你')
        send_time = ctx.message.created_at
        await ctx.message.add_reaction(ID.get_emoji_id(':tc_tongue:'))
        await ctx.send(f'{ctx.author.mention} {get_greeting_response("早安", send_time)}')
        exp = get_extra_exp(ctx, exp)
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, exp), ctx.author)

    @commands.command(brief="跟 TK4 說午安", help="!午安\n在不同時間會有不同的反應，等你來發掘!")
    async def 午安(self, ctx):
        exp = 10
        log.info(f'{ctx.author} 午安!!')
        send_time = ctx.message.created_at
        await ctx.message.add_reaction(ID.get_emoji_id(':tc_tongue:'))
        await ctx.send(f'{ctx.author.mention} {get_greeting_response("午安", send_time)}')
        exp = get_extra_exp(ctx, exp)
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, exp), ctx.author)

    @commands.command(brief="跟 TK4 說晚安", help="!晚安\n在不同時間會有不同的反應，等你來發掘!")
    async def 晚安(self, ctx):
        exp = 10
        log.info(f'{ctx.author} 去睡覺了')
        send_time = ctx.message.created_at
        await ctx.message.add_reaction(ID.get_emoji_id(':tc_tongue:'))
        await ctx.send(f'{ctx.author.mention} {get_greeting_response("晚安", send_time)}')
        exp = get_extra_exp(ctx, exp)
        await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, exp), ctx.author)


    @commands.command(brief="讓 TK4 幫忙送食物給小徹", help="!吃 [給小徹吃的東西]\n看你給什麼 給喜歡的可能會加比較多親密度")
    async def 吃(self, ctx, food):
        try:
            exp = 10
            hateFood = ['多益','茄子','青椒']
            loveFood = ['香菜','布丁','咖喱']
            log.info(f'{ctx.author} 打算喂你吃 {food}')
            exp = get_extra_exp(ctx, exp)
            if (food == ""):
                await ctx.send(f'{ctx.author.mention} 想喂小徹什麽? {ID.get_emoji_id(":tc_tongue:")}')
            elif (food in hateFood):
                await ctx.send(f'小徹拒絕了 {ctx.author.mention} 用 {food} 喂食 {ID.get_emoji_id(":tc_angry:")}')
            elif(food in loveFood):
                await ctx.send(f'小徹接受了 {ctx.author.mention} 用 {food} 喂食 {ID.get_emoji_id(":tc_happy:")}')
                await LevelSystem.send_level_up_message(self, db.update_user_exp(ctx.author.id, exp), ctx.author)
            else:
                await ctx.send(f'原來 {ctx.author.mention} 喜歡吃 {food} {ID.get_emoji_id(":tc_is_husky:")}')
        except Exception as e:
            await ctx.send(f'AAA')
            log.error(f'Error: {e}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        # print(message.content)
        if 'TK4' in message.content:
            await message.channel.send('叫我咪?')
            
            
    async def add_my_command(self, name, response, brief, help, exp):
        @commands.command(name=name)
        async def fun(ctx):
            log.info(response)
            await ctx.send(response)
            await LevelSystem.send_level_up_message(ctx, db.update_user_exp(ctx.author.id, exp), ctx.author)
        self.bot.add_command(fun)
    
    
    # commands
    @commands.has_role(ROLE_HUSKY)
    @commands.guild_only()
    @commands.command(brief="新增臨時自訂指令，現在只有總裁本人能用", help="!add_command [指令名稱] [回覆] [說明] [幫助] [經驗值]")
    async def add_command(self, ctx, name, response, brief="", help="", exp=10):
        await self.add_my_command(name, response, brief, help, exp)
        response = re.sub(r'<(:\w+?:)\d+>', r'\1', response)
        command_db.add_command(name, response, brief, help, exp)
        await ctx.send(f'Add command {name}')
    
    
    async def add_command_from_database(self):
        for name, info in command_reply_dict.items():
            brief = info[1]
            help = info[2]
            @commands.command(name=name, brief=brief, help=help)
            async def fun(ctx):
                command_name = ctx.command.name
                command_db.update_counter(command_name, ctx.message.created_at, command_db.DISCORD)
                exp = command_reply_dict[command_name][3]
                response = command_reply_dict[command_name][0]
                total = command_db.total_count(command_name, command_db.DISCORD)
                response = replace_emoji_dc(response)
                response = response.replace("username", f'{ctx.author.mention}').replace("total", str(total))
                exp = get_extra_exp(ctx, exp)
                await ctx.send(response)
                await LevelSystem.send_level_up_message(ctx, db.update_user_exp(ctx.author.id, exp), ctx.author)

            self.bot.add_command(fun)
    

            
# 要用 async await 
async def setup(bot):
    await bot.add_cog(FunnyCommands(bot))


# bot 前面記得加 self