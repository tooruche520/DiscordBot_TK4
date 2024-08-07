from discord.ext import commands, tasks
import logging as log
import modules.database.IdCollectionDatabase as ID

ROLE_DEVELOPER = ID.get_role_id("TK4開發團隊")
ROLE_HUSKY = ID.get_role_id("偉大的哈士奇總裁")

class ErrorMessage(commands.Cog, description="錯誤指令處理"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'TK4還小，這個指令還不太懂汪 {ID.get_emoji_id(":tc_sad:")}')
        
        elif isinstance(error, commands.MissingRole):
            if error.missing_role == ROLE_DEVELOPER:
                await ctx.send(f'很抱歉，你沒有權限使用此指令 {ID.get_emoji_id(":tc_sad:")}\n若你想成為開發者貢獻一份心力，請聯絡小徹')
            if error.missing_role == ROLE_HUSKY:
                await ctx.send(f'不好意思，請不要冒充小徹壞壞 {ID.get_emoji_id(":tc_angry:")}\n若你想成為小徹，很抱歉TK4我也沒辦法幫你 {ID.get_emoji_id(":tc_sad:")}')
            
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f'你現在在私人頻道!!\n要使用該指令，請至漏電攝影棚使用 {ID.get_emoji_id(":tc_tongue:")}')

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'你好像漏打了什麼東西，要不要使用 `!help` 檢查一下 {ID.get_emoji_id(":tc_is_husky:")}')
            
        else:
            await ctx.send(f'窩 窩不知道這是什麼意思 {ID.get_emoji_id(":tc_sad:")}')
            # await ctx.send(error)
            
        log.info(error)
 
    
           
# 要用 async await 
async def setup(bot):
    await bot.add_cog(ErrorMessage(bot))
