from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from dotenv import dotenv_values
import logging as log
import websockets
import requests
import json
import asyncio

config = dotenv_values(".env")
TWITCH_APP_ID = config.get("TWITCH_APP_ID")
TWITCH_APP_SECRET = config.get("TWITCH_APP_SECRET")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MODERATE]

class WSClient():
    def __init__(self):
        self.SESSION_ID = ""
 
    async def start_client(self):
        async with websockets.connect('ws://localhost:8080/eventsub') as websocket:
            data = await websocket.recv()
            data = json.loads(data)
            # print(type(data))
            self.SESSION_ID = data["payload"]["session"]["id"]
            # log.info(SESSION_ID)
            
            twitch = await Twitch(TWITCH_APP_ID, TWITCH_APP_SECRET)
            auth = UserAuthenticator(twitch, USER_SCOPE)
            token, refresh_token = await auth.authenticate()
            # print(token, refresh_token)
            await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
            self.API_HEADERS = {
                'Client-ID': TWITCH_APP_ID,
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            }
            
            self.subscribe_event()
            await self.loop(websocket)
            


    def subscribe_event(self):
        sub_channel_follow = {
            "type": "channel.follow",
            "version": "1",
            "condition": {"broadcaster_user_id": "790529577"},
            "transport": {
                "method": "websocket",
                "session_id": self.SESSION_ID
            }
        }
        
        sub_channel_ban = {
            "type": "channel.ban",
            "version": "1",
            "condition": {"broadcaster_user_id": "790529577"},
            "transport": {
                "method": "websocket",
                "session_id": self.SESSION_ID
            }
        }
        
        sub_channel_unban = {
            "type": "channel.unban",
            "version": "1",
            "condition": {"broadcaster_user_id": "790529577"},
            "transport": {
                "method": "websocket",
                "session_id": self.SESSION_ID
            }
        }
        
        url  = 'https://api.twitch.tv/helix/eventsub/subscriptions'
        response = requests.Session().post(url, headers=self.API_HEADERS, json=sub_channel_ban)
        # print(response.json())
        response = requests.Session().post(url, headers=self.API_HEADERS, json=sub_channel_unban)
        # print(response.json())
        response = requests.Session().post(url, headers=self.API_HEADERS, json=sub_channel_follow)
        # print(response.json())
        log.info("Successfully created subscription.")

    async def loop(self, websocket):
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            if(data["metadata"]["message_type"] == "session_keepalive"):
                continue
            if(data["metadata"]["message_type"] == "session_reconnect"):
                continue
            sub_type = data["payload"]["subscription"]["type"]
            if(sub_type == "channel.follow"):
                name = data["payload"]["event"]["user_name"]
                log.info(f'{name} now is follow!!')
                # await channel.send(f'感謝 {name}(twitch) 追隨!!')
                continue
            if(sub_type == "channel.ban"):
                name = data["payload"]["event"]["user_name"]
                reason = data["payload"]["event"]["reason"]
                log.info(f'{name} has banned!! Reason:{reason}')
                # await channel.send(f'{name} 因為 {reason} 被ban台了!!')
                continue
            if(sub_type == "channel.unban"):
                name = data["payload"]["event"]["user_name"]
                log.info(f'{name} has unbanned!!')
                # await channel.send(f'恭喜 {name} 解ban，歡回uwub')
                continue
            # print(f"\n\n{data}")
            
myClient = WSClient()
asyncio.run(myClient.start_client())