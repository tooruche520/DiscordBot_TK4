import discord
import requests
import time
import aiohttp
import logging as log
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get
from src.Id_collection import channle_id, emoji_list, role_list
from dotenv import dotenv_values

config = dotenv_values(".env")
TWITCH_APP_ID = config.get("TWITCH_APP_ID")
TWITCH_APP_SECRET = config.get("TWITCH_APP_SECRET")
CHANNLE_ID_NOTIFICATION = channle_id['開台通知']
ROLE_NOTIFIACTION = role_list['優質圖奇觀眾']
EMOJI_TC_HAPPY = emoji_list[':tc_happy:']

class StreamingNotifaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_started_at = '2022-10-12T02:38:03Z'

        body = {
            'client_id': TWITCH_APP_ID,
            'client_secret': TWITCH_APP_SECRET,
            "grant_type": 'client_credentials'
        }

        r = requests.post('https://id.twitch.tv/oauth2/token', body)
        keys = r.json()
        # print(f'key= {keys}')

        # Authentication with Twitch API.
        
        self.API_HEADERS = {
            'Client-ID': TWITCH_APP_ID,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': 'Bearer ' + keys['access_token']
        }

    async def checkuser(self, user):
        try:
            TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams?{}"
            url = TWITCH_STREAM_API_ENDPOINT_V5.format(f"user_login={user}")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.API_HEADERS) as req:
                        jsondata = await req.json()
                        # print(jsondata)
                        for info in jsondata['data']:
                            # print(f'{info["user_name"]} is streaming!')
                            return True, jsondata
                        else:
                            # print(f'{user} is not streaming!')
                            return False, None    
            except Exception as e:
                log.error("Error checking user: ", e)
                return False, None
        except IndexError:
            return False, None

    

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        twitch = Twitch(TWITCH_APP_ID, TWITCH_APP_SECRET)
        await twitch.authenticate_app([])
        log.info('Notifaction loop is on activity')
        @tasks.loop(seconds=40)
        async def live_notifs_loop():
            guild = self.bot.get_guild(1028268840112640100)
            role = guild.get_role(ROLE_NOTIFIACTION)
            
            twitch_name = 'tooruche520'

            status, response = await self.checkuser(twitch_name)

            # global last_started_at
            if status is True :
                current_start_time = response["data"][0]["started_at"]
                if current_start_time != self.last_started_at:
                    self.last_started_at = current_start_time
                    embed = await self.embed_notification(response)
                    channel = self.bot.get_channel(CHANNLE_ID_NOTIFICATION)
                    await channel.send(content=f"{role.mention} 小徹開台啦! 快來跟小徹一起玩吧{EMOJI_TC_HAPPY}", embed=embed)
                    log.info(f"{twitch_name} started streaming. Sending a notification.")

        live_notifs_loop.start()

    
    async def embed_notification(self, response):
        
        title = response["data"][0]['title']
        user_name = response["data"][0]['user_name']
        thumbnail_url = response["data"][0]['thumbnail_url'].replace("{width}", "1920").replace("{height}", "1080")
        viewer_count = response["data"][0]['viewer_count']
        
        user_profile_image = ""
        url = "https://api.twitch.tv/helix/users?login=tooruche520"
        try:
            jsondata = requests.Session().get(url, headers=self.API_HEADERS).json()
            user_profile_image = jsondata["data"][0]['profile_image_url']
        except Exception as e:
            log.warning("Could not get user information")

        game_id = response["data"][0]['game_id']
        game_name = ""
        url = "https://api.twitch.tv/helix/games?{}"
        url = url.format(f"id={game_id}")
        # print(url)
        try:
            jsondata = requests.Session().get(url, headers=self.API_HEADERS).json() 
            # print(jsondata)
            game_name = jsondata["data"][0]['name'] 
        except Exception as e:
            log.warning("Could not get user information")
            game_name = "聊天"

        # log.info(thumbnail_url)
        
        # title = response["data"][0]['']
        # title = response["data"][0]['']

        current_time = time.strftime("%Y/%m/%d %H:%M", time.localtime()) 

        embed=discord.Embed(title=title, url="https://www.twitch.tv/tooruche520", color=0x9146ff, description="[小徹的直播](https://www.twitch.tv/tooruche520)")
        embed.set_author(name=user_name, icon_url=user_profile_image)
        embed.set_image(url=thumbnail_url)
        embed.add_field(name="Game ", value=game_name, inline=True)
        embed.add_field(name="viewer ", value=viewer_count, inline=True)
        embed.set_footer(text=f'TK4叫你去看台uwu · {current_time}')
        # await channel.send(embed=embed)
        return embed


# 要用 async await 
async def setup(bot):
    await bot.add_cog(StreamingNotifaction(bot))


# bot 前面記得加 self

