# 流程簡單記一下
# 首先我先傳一則訊息，然後拿到message_id
# 拿到之後修改檔案，重新啟動TK4，下方on_ready方法會自動增加表情符號


from discord.ext import commands 

import logging as log
import modules.database.IdCollectionDatabase as ID


CHANNEL_ID_GET_ROLES = ID.get_channel_id('領取身分組')
MESSAGE_ID_GET_ROLES = ID.get_message_id('領取身分組訊息')

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        msg = await self.bot.get_channel(CHANNEL_ID_GET_ROLES).fetch_message(MESSAGE_ID_GET_ROLES)
        await msg.add_reaction(str(ID.get_emoji_id(':tc_happy:')))
        await msg.add_reaction(str(ID.get_emoji_id(':tc_is_husky:')))        
        await msg.add_reaction(str(ID.get_emoji_id(':tc_tongue:')))
        
    # event
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != MESSAGE_ID_GET_ROLES:
            return

        async def add_reaction(self, payload, emoji_name, role_name):
            if str(payload.emoji) != str(ID.get_emoji_id(emoji_name)):
                return
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(int(ID.get_role_id(role_name)))
            await payload.member.add_roles(role)
            log.info(f"{payload.member} get the role {role_name}")

        await add_reaction(self, payload, ':tc_happy:', '普通人')
        await add_reaction(self, payload, ':tc_is_husky:', '小色鬼')
        await add_reaction(self, payload, ':tc_tongue:', '優質圖奇觀眾')

    # event
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != MESSAGE_ID_GET_ROLES:
            return

        async def remove_reaction(self, payload, emoji_name, role_name):
            if str(payload.emoji) != str(ID.get_emoji_id(emoji_name)):
                return
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(int(ID.get_role_id(role_name)))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
            log.info(f"{member} loss the role {role_name}")

        await remove_reaction(self, payload, ':tc_happy:', '普通人')
        await remove_reaction(self, payload, ':tc_is_husky:', '小色鬼')
        await remove_reaction(self, payload, ':tc_tongue:', '優質圖奇觀眾')



# 要用 async await 
async def setup(bot):
    await bot.add_cog(ReactionRole(bot))

# bot 前面記得加 self
