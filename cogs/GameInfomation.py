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

@dataclass
class SwGameType:
    name: str
    og_data_title: str
    channle_id: int

class GameInfomation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sw_game_list = []
        self.sw_game_list.append(
            SwGameType("splatoon3", "最新フェス情報 に第3回フェス結果を追加!", CHANNLE_GAME_SPLATOON), 
            SwGameType("pokemon_sv", "https://appmedia.jp/pokemon_sv/76185673", CHANNLE_GAME_POKEMONSV),
        )
        
    def get_newest_data(self, sw_game):
        response = requests.get("https://appmedia.jp/splatoon3")
        # response = requests.get("https://appmedia.jp/pokemon_sv")
        soup = BeautifulSoup(response.text, "html.parser")
        node1 = soup.find(lambda tag: tag.name=="h3" and "更新記事" in tag.text).find_next_sibling().table.tbody

        result_list = node1.find_all("tr")

        for news in result_list:
            if news.th is not None:
                result_list.remove(news)
                continue
        for news in result_list:
            if news.td.find_next_sibling().a is None:
                result_list.remove(news)
                continue

        get_data_list = []
        for i, news in enumerate(result_list):
            tag = news.td.div.text
            new = news.td.find_next_sibling().a
            if i==0:
                newest_data_title = new.text
            if(new.text == og_data_title):
                if og_data_title == newest_data_title:
                    # print("Data is newest, no print result")
                    # return None, None, None
                    pass
                else:
                    og_data_title = newest_data_title
                break
            else:
                get_data_list.append(tag, new.text, (new['href']))
        return get_data_list
        

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        # sw_game_list = []
        # sw_game_list.append(
        #     SwGameType("splatoon3", "https://appmedia.jp/splatoon3/76335097", CHANNLE_GAME_SPLATOON), 
        #     SwGameType("pokemon_sv", "https://appmedia.jp/pokemon_sv/76185673", CHANNLE_GAME_POKEMONSV),
        # )
        
        @tasks.loop(hours=8)
        async def loop_get():
            for sw_game in self.sw_game_list:
                # role = guild.get_role(sw_game.channle_id)
                data_list = self.get_newest_data(sw_game)
                for data in data_list:
                    print(data[0], data[1], data[2])
                    channel = self.bot.get_channel(sw_game.channle_id)
                    await channel.send(f"【{data[0]}】{data[1]}\n{data[2]}")
                
        loop_get().start()
        
    

# 要用 async await 
async def setup(bot):
    await bot.add_cog(GameInfomation(bot))


# bot 前面記得加 self

