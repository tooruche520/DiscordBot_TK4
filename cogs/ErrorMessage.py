from discord.ext import commands, tasks
import logging as log
from src.Id_collection import channle_id, emoji_list, role_list

ROLE_HUSKY = role_list["偉大的哈士奇總裁"]
ROLE_DEVELOPER = role_list["TK4開發團隊"]

class ErrorMessage(commands.Cog, description="錯誤指令處理"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'窩 窩不知道這是什麼意思 {emoji_list["tc_sad"]}')
        
        elif isinstance(error, commands.MissingRole):
            if error.missing_role == ROLE_DEVELOPER:
                await ctx.send(f'很抱歉，你沒有權限使用此指令 {emoji_list["tc_sad"]}\n若你想成為開發者貢獻一份心力，請聯絡小徹')
            if error.missing_role == ROLE_HUSKY:
                await ctx.send(f'不好意思，請不要冒充小徹壞壞 {emoji_list["tc_angry"]}\n若你想成為小徹，很抱歉TK4我也沒辦法幫你 {emoji_list["tc_sad"]}')
            
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f'你現在在私人頻道!!\n要使用該指令，請至漏電攝影棚使用 {emoji_list["tc_tongue"]}')
        else:
            await ctx.send(f'你要不要聽聽看你在說甚麼 {emoji_list["tc_sip"]}')
        # await ctx.send(f'Error! {emoji_list["tc_sad"]}')
        print(error)
 
    
           
# 要用 async await 
async def setup(bot):
    await bot.add_cog(ErrorMessage(bot))
