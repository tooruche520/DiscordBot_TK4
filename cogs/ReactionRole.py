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


    # 測試 function
    async def add_reaction(self, payload, emoji_name, role_name):
        # print(1)
        if str(payload.emoji) == str(self.emoji[emoji_name]):
            return
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(int(self.role_list[role_name]))
        await payload.member.add_roles(role)
        print(f"Added reaction {emoji_name}")


    # event
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)

        try:
            # 這裡出錯QQ
            await add_reaction(self, payload, 'tc_happy', '普通人')
        except Exception as e:
            print("Failed to add reaction") 
            print(e) 
            # name 'add_reaction' is not defined


        # 原本的寫法，這裡沒問題
        # if str(payload.emoji) == str(self.emoji['tc_happy']):
        #     # print(self.role_list['普通人'])
        #     role = guild.get_role(int(self.role_list['普通人']))
        #     await payload.member.add_roles(role)
        #     print("Added reaction tc_happy")

        
        if str(payload.emoji) == str(self.emoji['tc_is_husky']):
            # print(self.role_list['小色鬼'])
            role = guild.get_role(int(self.role_list['小色鬼']))
            await payload.member.add_roles(role)
            print("Added reaction tc_is_husky")
        # print(payload.emoji)



    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        
        if str(payload.emoji) == str(self.emoji['tc_happy']):
            role = guild.get_role(int(self.role_list['普通人']))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
            print("Removed reaction tc_happy")

        if str(payload.emoji) == str(self.emoji['tc_is_husky']):
            role = guild.get_role(int(self.role_list['小色鬼']))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
            print("Removed reaction tc_is_husky")



# 要用 async await 
async def setup(bot):
    await bot.add_cog(ReactionRole(bot))

# bot 前面記得加 self
