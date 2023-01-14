import discord
import requests
from bs4 import BeautifulSoup
import time
import logging as log
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get
from src.Id_collection import channle_id, emoji_list, role_list
from dotenv import dotenv_values
from dataclasses import dataclass

config = dotenv_values(".env")
CHANNLE_GAME_SPLATOON = channle_id["斯普拉遁"]
CHANNLE_GAME_POKEMONSV = channle_id["寶可夢朱紫"]

class TwitterNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    # event
    @commands.Cog.listener()
    async def on_ready(self):
       
        @tasks.loop()
        async def loop_get():
            pass
                
        loop_get().start()
        
    

# 要用 async await 
async def setup(bot):
    await bot.add_cog(TwitterNotification(bot))

