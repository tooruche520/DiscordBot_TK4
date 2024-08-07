import discord
import requests
from bs4 import BeautifulSoup
import time
import logging as log
from discord.ext import tasks, commands
import modules.database.IdCollectionDatabase as ID
from dotenv import dotenv_values
from dataclasses import dataclass
import modules.database.GameInfoDatabase as game_db
import aiohttp


config = dotenv_values(".env")
CHANNEL_GAME_SPLATOON = ID.get_channel_id("斯普拉遁")
CHANNEL_GAME_POKEMONSV = ID.get_channel_id("寶可夢朱紫")

@dataclass
class SwGameType:
    name: str
    og_data_title: str
    channel_id: int

class GameInfomation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sw_game_list = []
        self.sw_game_list.extend([
            SwGameType("splatoon3", game_db.get_newest_title("splatoon3"), CHANNEL_GAME_SPLATOON),            
            SwGameType("pokemon_sv", game_db.get_newest_title("pokemon_sv"), CHANNEL_GAME_POKEMONSV)]
        )
        # self.sw_game_list.append(
        #     SwGameType("splatoon3", "最新フェス情報 に第3回フェス結果を追加!", CHANNEL_GAME_SPLATOON)
        # )
        # self.sw_game_list.append(
        #     SwGameType("pokemon_sv", "サーフゴーの育成論と対策 を公開", CHANNEL_GAME_POKEMONSV)
        # )
        
    async def get_newest_data(self, sw_game):
        url = ""
        if (sw_game.name == "splatoon3"):
            url = "https://appmedia.jp/splatoon3"
        elif (sw_game.name == "pokemon_sv"):
            url = "https://appmedia.jp/pokemon_sv"
            
        # response = requests.get(url)
        # response = requests.get("https://appmedia.jp/pokemon_sv")  
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
                try:
                    node1 = soup.find(lambda tag: tag.name=="h3" and "更新記事" in tag.text).find_next_sibling().table.tbody
                except Exception as e:
                    log.error(e)
                    return []

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
                    if(new.text == sw_game.og_data_title):
                        if sw_game.og_data_title == newest_data_title:
                            # print("Data is newest, no print result")
                            # return None, None, None
                            pass
                        else:
                            sw_game.og_data_title = newest_data_title
                            game_db.update_newest_title(sw_game.name, newest_data_title)
                        break
                    else:
                        get_data_list.append((tag, new.text, new['href']))
                return get_data_list
        

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        # sw_game_list = []
        # sw_game_list.append(
        #     SwGameType("splatoon3", "https://appmedia.jp/splatoon3/76335097", CHANNEL_GAME_SPLATOON), 
        #     SwGameType("pokemon_sv", "https://appmedia.jp/pokemon_sv/76185673", CHANNEL_GAME_POKEMONSV),
        # )
        
        @tasks.loop(minutes=10)
        async def loop_get():
            # print(self.sw_game_list)
            for sw_game in self.sw_game_list:
                # role = guild.get_role(sw_game.channel_id)
                # print(sw_game)
                data_list = await self.get_newest_data(sw_game)
                channel = self.bot.get_channel(sw_game.channel_id)
                for data in data_list:
                    print(sw_game.name, data[0], data[1], data[2])
                    await channel.send(f"【{data[0]}】{data[1]}\n{data[2]}")
                
        loop_get.start()
        
    @commands.command()
    async def getGameNews(self, ctx):
        for sw_game in self.sw_game_list:
            data_list = await self.get_newest_data(sw_game)
            channel = self.bot.get_channel(sw_game.channel_id)
            for data in data_list:
                print(sw_game.name, data[0], data[1], data[2])
                await channel.send(f"【{data[0]}】{data[1]}\n{data[2]}")
    

# 要用 async await 
async def setup(bot):
    await bot.add_cog(GameInfomation(bot))


# bot 前面記得加 self

