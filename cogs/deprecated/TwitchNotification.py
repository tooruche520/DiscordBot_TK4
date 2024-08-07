import discord
import logging as log
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get
import websockets
import requests
import json
import asyncio
import time
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from dotenv import dotenv_values
import modules.database.IdCollectionDatabase as ID
from dotenv import dotenv_values

CHANNEL_ID_WELCOME = ID.get_channel_id["歡迎入口"]
config = dotenv_values(".env")
TWITCH_APP_ID = config.get("TWITCH_APP_ID")
TWITCH_APP_SECRET = config.get("TWITCH_APP_SECRET")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MODERATE]

# wss://eventsub-beta.wss.twitch.tv/ws

class TwitchNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

            
    # event
    @commands.Cog.listener()
    async def on_ready(self):
        
        await asyncio.sleep(10)
        twitch = await Twitch(TWITCH_APP_ID, TWITCH_APP_SECRET)
        auth = UserAuthenticator(twitch, USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        # print(token, refresh_token)
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        
        async def new_websocket_connection(self, url, token, isFirstTime):
            async with websockets.connect(url) as websocket:
                try:
                    log.info("Successfully connected to webcocket.")
                    if isFirstTime:
                        
                        data = await websocket.recv()
                        data = json.loads(data)
                        # print(type(data))
                        SESSION_ID = data["payload"]["session"]["id"]
                        # log.info(SESSION_ID)
                        
                        API_HEADERS = {
                            'Client-ID': TWITCH_APP_ID,
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token
                        }
                        
                        sub_channel_follow = {
                            "type": "channel.follow",
                            "version": "1",
                            "condition": {"broadcaster_user_id": "790529577"},
                            "transport": {
                                "method": "websocket",
                                "session_id": SESSION_ID
                            }
                        }
                        
                        sub_channel_ban = {
                            "type": "channel.ban",
                            "version": "1",
                            "condition": {"broadcaster_user_id": "790529577"},
                            "transport": {
                                "method": "websocket",
                                "session_id": SESSION_ID
                            }
                        }
                        
                        sub_channel_unban = {
                            "type": "channel.unban",
                            "version": "1",
                            "condition": {"broadcaster_user_id": "790529577"},
                            "transport": {
                                "method": "websocket",
                                "session_id": SESSION_ID
                            }
                        }
                        
                        url  = 'https://api.twitch.tv/helix/eventsub/subscriptions'
                        response = requests.Session().post(url, headers=API_HEADERS, json=sub_channel_ban)
                        # print(response.json())
                        response = requests.Session().post(url, headers=API_HEADERS, json=sub_channel_unban)
                        # print(response.json())
                        response = requests.Session().post(url, headers=API_HEADERS, json=sub_channel_follow)
                        # print(response.json())
                        log.info("Successfully created subscription.")
                    channel = self.bot.get_channel(CHANNEL_ID_WELCOME)
                    while True:
                        data = await websocket.recv()
                        data = json.loads(data)
                        if(data["metadata"]["message_type"] == "session_keepalive"):
                            continue
                        if(data["metadata"]["message_type"] == "session_welcome"):
                            continue
                        if(data["metadata"]["message_type"] == "session_reconnect"):
                            log.warn("Session will reconnect.")
                            new_url = data["payload"]["session"]["reconnect_url"]
                            asyncio.create_task(new_websocket_connection(self, new_url, token, False))
                            await asyncio.sleep(5)
                            await websocket.close()
                            log.info("Original Session closed!!")
                            break
                        sub_type = data["payload"]["subscription"]["type"]
                        if(sub_type == "channel.follow"):
                            name = data["payload"]["event"]["user_name"]
                            log.info(f'{name} now is follow!!')
                            await channel.send(f'感謝 {name}(twitch) 追隨!!')
                            continue
                        if(sub_type == "channel.ban"):
                            name = data["payload"]["event"]["user_name"]
                            reason = data["payload"]["event"]["reason"]
                            log.info(f'{name} has banned!! Reason:{reason}')
                            await channel.send(f'{name} 因為 {reason} 被ban台了!!')
                            continue
                        if(sub_type == "channel.unban"):
                            name = data["payload"]["event"]["user_name"]
                            log.info(f'{name} has unbanned!!')
                            await channel.send(f'恭喜 {name} 解ban，歡回uwub')
                            continue
                except Exception as e:    
                    log.error(e)    
                    await asyncio.sleep(10)
                    url = 'wss://eventsub-beta.wss.twitch.tv/ws'
                    await new_websocket_connection(self, url, token, True)
        
        
        url = 'wss://eventsub-beta.wss.twitch.tv/ws'
        await new_websocket_connection(self, url, token, True)
        
    

# 要用 async await 
async def setup(bot):
    await bot.add_cog(TwitchNotification(bot))

