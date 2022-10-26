from discord.ext import commands 
import discord
import json
import logging as log
from src.Id_collection import channle_id, emoji_list

CHANNLE_ID_WELCOME = channle_id["TK4開發測試頻道"]
CHANNLE_ID_GET_ROLES = channle_id["領取身分組頻道"]

class Grettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_member_join(self, member):
        log.info(f'{member} join')
        channel = self.bot.get_channel(CHANNLE_ID_WELCOME)
        Identity = self.bot.get_channel(CHANNLE_ID_GET_ROLES)
        await channel.send(f'恭喜 {member.mention} 踏入漏電的第一步\n請至 **{Identity.mention}** 領取你的身分組')

    # event
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await member.guild.fetch_ban(member)
            log.info(f'{member} banned')
            channel = self.bot.get_channel(CHANNLE_ID_WELCOME)
            await channel.send(f'{member.mention} 受到了十萬伏特攻擊，搶救無效，被TK4送到攝影棚外面')
        except:
            log.info(f'{member} leave')
            channel = self.bot.get_channel(CHANNLE_ID_WELCOME)
            await channel.send(f'噢不， {member.mention} 的電漏光了')


# 要用 async await 
async def setup(bot):
    await bot.add_cog(Grettings(bot))

# bot 前面記得加 self
