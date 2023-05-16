from discord.ext import commands, tasks
from discord.user import User
import os
import asyncio
import logging as log
from datetime import datetime, date, time, timedelta
from src.Id_collection import role_list, emoji_list, channle_id
import sqlite3
# import modules.MyDatabase as db

ROLE_DEVELOPER = role_list["TK4開發團隊"]
CHANNLE_HBD = channle_id["生日快樂"]


# 資料庫連線設定
conn = sqlite3.connect('src/database/birthday.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS birthdays
             (user_id INTEGER PRIMARY KEY, name TEXT, birth_year TEXT, birth_date TEXT, show_age INTEGER)''')


class HappyBirthday(commands.Cog, description="TK4祝尼生日快樂uwu"):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays_loop.start()
        

    @commands.command(name='生日', help='登記生日：!生日 生日(YYYY-MM-DD) 是否公開歲數(Y/N)')
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
            channel = self.bot.get_channel(CHANNLE_HBD) # 請填入你要傳送訊息的頻道ID
            if show_age:
                await channel.send('祝 {} {}歲 生日快樂!!'.format(name, age))
            else:
                await channel.send('祝 {} 生日快樂!!'.format(name))
    
    @check_birthdays_loop.before_loop
    async def before_check_birthdays_loop(self):
        await self.bot.wait_until_ready()
        log.info('waiting time')
        now = datetime.now()
        then = datetime.combine(now, time(0, 0, 0)) #TODO: 改時間
        if then < now :
            then += timedelta(days=1)
        wait_time = (then - now).total_seconds()
        print(now)
        print(then)
        log.info('waiting time: {}'.format(wait_time))
        await asyncio.sleep(wait_time)
        log.info('wait time finished: {}'.format(wait_time))

# 要用 async await 
async def setup(bot):
    await bot.add_cog(HappyBirthday(bot))

# bot 前面記得加 self
