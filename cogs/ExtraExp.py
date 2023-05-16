import discord
from discord.ext import commands
from discord.utils import get
from src.Id_collection import channle_id, emoji_list, role_list
from modules.MyDatabase import edit_user_twitch_account


class ExtraExp(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(brief="登記你的Twitch ID", help="!twitch_id [你的ID]\n在不同時間會有不同的反應，等你來發掘!")
    async def twitch_id(self, ctx, twitch_id):
        edit_user_twitch_account(ctx.author.id, twitch_id)
        await ctx.send(f"已將您的Twitch ID `{twitch_id}` 登記至資料庫!!")


async def setup(bot:commands.Bot):
    await bot.add_cog(ExtraExp(bot))
    
def get_extra_exp(ctx, exp):
    user_roles = ctx.author.roles
    # 判斷使用者是否擁有名為'Birthday Role'的身分組
    for role in user_roles:
        if role.name == '飼養員':
            return exp
        if role.name == '訂閱一級領養':
            return exp*1.2
        if role.name == '訂閱二級領養':
            return exp*1.4
        if role.name == '訂閱三級領養':
            return exp*2
    return exp
