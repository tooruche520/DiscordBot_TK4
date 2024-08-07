from discord.ext import tasks, commands 
import logging as log
import modules.database.IdCollectionDatabase as ID
from modules.LimitCounter import clear, sub_count
import modules.database.UserDatabase as db
from modules.database.UserDatabase import User


CHANNEL_ID_LEVEL = ID.get_channel_id("升等通知")

class LevelSystem(commands.Cog, description="TK4愛你系統"):
    def __init__(self, bot):
        self.bot = bot

    async def send_level_up_message(self, is_upgrade, user):
        if(is_upgrade):
            channel = self.bot.get_channel(CHANNEL_ID_LEVEL)
            user_data = db.get_user_by_userid(user.id)
            level = user_data.level
            await channel.send(f'跟 {user.mention} 的好感度達到了 {level} 級!!')
        return
    
    # async def send_level_up_message_test(self, is_upgrade, level, user):
    #     if(is_upgrade):
    #         channel = self.bot.get_channel(CHANNEL_ID_LEVEL)
    #         # user_data = user
    #         # level = user_data.level
    #         await channel.send(f'{user.mention} 升到了第{level}等')
    #     return

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                db.add_user(User(member.id))
        log.info(f"Successfully add all user from Server")

        @tasks.loop(hours=1)
        async def clear_task():
            clear()
        clear_task.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if member.bot:
            return;
        
        user_id = member.id
        user_adoption = User.Adoption.GENERAL
        db.add_user(User(user_id, user_adoption))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        try:
            if message.content[0] == '!':
                return
        except IndexError:
            log.info('This message no content')

        sub_count(message.author.id)
        await self.send_level_up_message(db.update_user_exp(message.author.id, 2), message.author)
        

    @commands.command(brief="查看TK4有多愛你", help="!level")
    @commands.guild_only()
    async def level(self, ctx):
        user_data = db.get_user_by_userid(ctx.author.id)
        level = user_data.level
        experience = user_data.experience
        await ctx.send(f'{ctx.author.mention} 目前是等級{level}，累積了{experience}點親密度!!')


# 要用 async await 
async def setup(bot):
    await bot.add_cog(LevelSystem(bot))

