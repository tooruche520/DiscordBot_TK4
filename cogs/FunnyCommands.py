from discord.ext import commands 
import discord


class Grettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    @commands.command()
    async def 棒棒糖(self, ctx):
        print(f'{ctx.author}給了TK4一根棒棒糖')
        await ctx.send(f'謝謝{ctx.author.mention}的棒棒糖')

# 要用 async await 
async def setup(bot):
    await bot.add_cog(Grettings(bot))


# bot 前面記得加 self