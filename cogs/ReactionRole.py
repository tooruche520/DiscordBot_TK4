from discord.ext import commands 
import discord
import json
import logging as log

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open('data.json', "r", encoding = "utf8") as file:
            data = json.load(file)
            self.channel_role = data['TK4開發測試頻道']
            self.emoji = data["emoji_list"]
            self.role_list = data["role_list"]
            self.message_role = int(data["領取身分組訊息"])


    @commands.Cog.listener()
    async def on_ready(self):
        msg = await self.bot.get_channel(int(self.channel_role)).fetch_message(self.message_role)
        await msg.add_reaction(str(self.emoji['tc_happy']))
        await msg.add_reaction(str(self.emoji['tc_is_husky']))        
        await msg.add_reaction(str(self.emoji['tc_tongue']))
        

    # event
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.message_role:
            return

        async def add_reaction(self, payload, emoji_name, role_name):
            if str(payload.emoji) != str(self.emoji[emoji_name]):
                return
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(int(self.role_list[role_name]))
            await payload.member.add_roles(role)
            log.info(f"{payload.member} get the role {role_name}")

        await add_reaction(self, payload, 'tc_happy', '普通人')
        await add_reaction(self, payload, 'tc_is_husky', '小色鬼')
        await add_reaction(self, payload, 'tc_tongue', '優質圖奇觀眾')

    # event
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self.message_role:
            return

        async def remove_reaction(self, payload, emoji_name, role_name):
            if str(payload.emoji) != str(self.emoji[emoji_name]):
                return
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(int(self.role_list[role_name]))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
            log.info(f"{member} loss the role {role_name}")

        await remove_reaction(self, payload, 'tc_happy', '普通人')
        await remove_reaction(self, payload, 'tc_is_husky', '小色鬼')
        await add_reaction(self, payload, 'tc_tongue', '優質圖奇觀眾')



# 要用 async await 
async def setup(bot):
    await bot.add_cog(ReactionRole(bot))

# bot 前面記得加 self
