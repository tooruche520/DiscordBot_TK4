from discord.ext import commands, tasks
import discord
from discord.user import User
import os
import asyncio
import logging as log
from datetime import datetime, date, time, timedelta
import modules.database.IdCollectionDatabase as ID
import sqlite3
# import modules.database.UserDatabase as db

ROLE_DEVELOPER = ID.get_role_id("TK4開發團隊")
CHANNEL_HBD = ID.get_channel_id("生日快樂")
EMOJI_BALL = ID.get_emoji_id(":tc_ball:")


# 資料庫連線設定
conn = sqlite3.connect('database/birthday.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS birthdays
             (user_id INTEGER PRIMARY KEY, name TEXT, birth_year TEXT, birth_date TEXT, show_age INTEGER)''')


class HappyBirthday(commands.Cog, description="TK4祝尼生日快樂uwu"):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays_loop.start()
        

    @commands.command(brief="登記生日，讓TK4祝尼生日快樂uwu", name='生日', help='登記生日：!生日 生日(YYYY-MM-DD) 是否公開歲數(Y/N)')
    async def add_birthday(self, ctx, birth_date: str, show_age: str):
        user_id = ctx.author.id
        name = ctx.author.name
        if show_age.upper() == 'Y':
            show_age = 1
        elif show_age.upper() == 'N':
            show_age = 0
        else:
            await ctx.send('公開歲數的輸入參數僅可輸入大小寫Y與N，Y表示同意公開歲數，N為不公開歲數')
            return
        # 將生日資料寫入資料庫
        birth_date = date.fromisoformat(birth_date)
        birth_year_datetime = birth_date.year
        birth_date_datetime = f"{birth_date.month}-{birth_date.day}"
        c.execute("INSERT OR REPLACE INTO birthdays (user_id, name, birth_year, birth_date, show_age) VALUES (?, ?, ?, ?, ?)",
                  (user_id, name, birth_year_datetime, birth_date_datetime, show_age))
        conn.commit()
        log.info(f"Updated birthdays: {name}")
        await ctx.send('生日資料已成功登記！')


    @tasks.loop(hours=24) #TODO: 改時間
    async def check_birthdays_loop(self):
        # 取得現在的日期
        today = date.today()
        today_date = f"{today.month}-{today.day}"
        # print(today_date)
        # 取得明天的日期
        c.execute(f"SELECT * FROM birthdays WHERE birth_date='{today_date}'")
        birthdays = c.fetchall()
        log.info(birthdays)
        for user_id, name, birth_year, birth_date, show_age in birthdays:
            # 計算年齡
            age = today.year - int(birth_year)
            # 傳送生日祝福訊息到指定頻道
            channel = self.bot.get_channel(CHANNEL_HBD) # 請填入你要傳送訊息的頻道ID
            user = self.bot.get_user(user_id)
            if show_age:
                await channel.send(f'祝{user.mention} {age}歲 生日快樂!!')
                embed = discord.Embed(\
                    title=f"{name}生日快樂!!", \
                    description=f"今天是{name}的{age}歲生日!! \n快祝他生日快樂吧", \
                    color=0xFC7B0A \
                )
                embed.add_field(name=f"{age}歲 生日快樂汪", value=f"嗷嗚~{EMOJI_BALL}", inline=False)
            else:
                await channel.send(f'祝{user.mention} 生日快樂!!')
                embed = discord.Embed(\
                    title=f"{name}生日快樂!!", \
                    description=f"今天是{name}的生日!! \n快祝他生日快樂吧", \
                    color=0xFC7B0A \
                )
                embed.add_field(name=f"生日快樂汪", value=f"嗷嗚~{EMOJI_BALL}", inline=False)
                
            embed.set_thumbnail(url=user.avatar)
            file = discord.File("src/pic/Heart.png", filename="heart.png")
            embed.set_image(url="attachment://heart.png")
            await channel.send(file=file, embed=embed)
        
    
    @check_birthdays_loop.before_loop
    async def before_check_birthdays_loop(self):
        await self.bot.wait_until_ready()
        log.info('waiting time')
        now = datetime.now()
        then = datetime.combine(now, time(0, 0, 0)) #TODO: 改時間
        if then < now :
            then += timedelta(days=1)
        wait_time = (then - now).total_seconds()
        # print(now)
        # print(then)
        log.info('waiting time: {}'.format(wait_time))
        await asyncio.sleep(wait_time)
        log.info('wait time finished: {}'.format(wait_time))

# 要用 async await 
async def setup(bot):
    await bot.add_cog(HappyBirthday(bot))

# bot 前面記得加 self
