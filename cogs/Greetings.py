from discord.ext import commands 
import discord
import json

with open('data.json', "r", encoding = "utf8") as file:
    data = json.load(file)

class Grettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open('data.json', "r", encoding = "utf8") as file:
            self.data = json.load(file)

    # event
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join')
        channel = self.bot.get_channel(int(self.data["TK4開發測試頻道"]))
        await channel.send(f'{member.mention} join')

    # event
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} leave')
        channel = self.bot.get_channel(int(self.data["TK4開發測試頻道"]))
        await channel.send(f'{member.mention} leave')

    # # commands
    # @commands.command()
    # async def 棒棒糖(self, ctx):
    #     print(f'{ctx.author}給了TK4一根棒棒糖')
    #     await ctx.send(f'謝謝{ctx.author.mention}的棒棒糖')

# 要用 async await 
async def setup(bot):
    await bot.add_cog(Grettings(bot))


# bot 前面記得加 self