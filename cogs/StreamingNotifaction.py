from discord.ext import commands 
import discord


class StreamingNotifaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def emtest(self, ctx):
        embed=discord.Embed(title="小徹今天居然...?! ", url="https://www.twitch.tv/tooruche520", description="今天清晨，在橋墩下的小徹居然在... ")
        embed.set_author(name="晴海徹 ", icon_url="https://pbs.twimg.com/profile_images/1578027096307249152/a6EglDE4_400x400.jpg ")
        embed.set_thumbnail(url="https://pbs.twimg.com/media/FaS7WCqVsAA6zar?format=jpg&name=4096x4096 ")
        embed.add_field(name="viewer ", value="1069 ", inline=False)
        await ctx.send(embed=embed)


# 要用 async await 
async def setup(bot):
    await bot.add_cog(StreamingNotifaction(bot))


# bot 前面記得加 self