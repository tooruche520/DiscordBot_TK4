from discord.ext import commands 
import discord
import json

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open('data.json', "r", encoding = "utf8") as file:
            data = json.load(file)
            self.emoji = data["emoji_list"]
            self.role_list = data["role_list"]
            self.message_role = int(data["領取身分組訊息"])


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
            print(f"{payload.member} get the role {role_name}")

        await add_reaction(self, payload, 'tc_happy', '普通人')
        await add_reaction(self, payload, 'tc_is_husky', '小色鬼')

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
            print(f"{member} loss the role {role_name}")

        await remove_reaction(self, payload, 'tc_happy', '普通人')
        await remove_reaction(self, payload, 'tc_is_husky', '小色鬼')



# 要用 async await 
async def setup(bot):
    await bot.add_cog(ReactionRole(bot))

# bot 前面記得加 self
