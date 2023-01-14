import asyncio
import websockets
import requests
import json
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from dotenv import dotenv_values

config = dotenv_values(".env")
TWITCH_APP_ID = config.get("TWITCH_APP_ID")
TWITCH_APP_SECRET = config.get("TWITCH_APP_SECRET")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.CHANNEL_MODERATE]

async def hello(uri):
    async with websockets.connect(uri) as websocket:
        data = await websocket.recv()
        data = json.loads(data)
        # print(type(data))
        SESSION_ID = data["payload"]["session"]["id"]
        # print(SESSION_ID)
        
        twitch = await Twitch(TWITCH_APP_ID, TWITCH_APP_SECRET)
        auth = UserAuthenticator(twitch, USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

        
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
        print("\n\nSuccessfully created subscription.")
        
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            if(data["metadata"]["message_type"] == "session_keepalive"):
                continue
            if(data["payload"]["subscription"]["type"] == "channel.follow"):
                print(f'{data["payload"]["event"]["user_name"]} now is follow!!\n')
                continue
            if(data["payload"]["subscription"]["type"] == "channel.ban"):
                name = data["payload"]["event"]["user_name"]
                reason = data["payload"]["event"]["reason"]
                print(f'{name} has banned!! Reason:{reason}\n')
                continue
            if(data["payload"]["subscription"]["type"] == "channel.unban"):
                name = data["payload"]["event"]["user_name"]
                print(f'{name} has unbanned!!\n')
                continue
            # print(f"\n\n{data}")
            
            

asyncio.get_event_loop().run_until_complete(hello('wss://eventsub-beta.wss.twitch.tv/ws'))



# from websocket import enableTrace, create_connection, WebSocketApp
# # import thread
# # import time

# def on_message(ws, message):
#     print('\n======received message======')
#     print(message)

# def on_error(ws, error):
#     print('\n======received error======')
#     print(error)

# def on_close(ws):
#     print("\n### closed ###")

# def on_open(ws):
#     print("\n### opened ###")


# enableTrace(True)
# ws=create_connection("wss://eventsub-beta.wss.twitch.tv/ws")
# result = ws.recv()
# print('Result: {}'.format(result))

# # ws = WebSocketApp("wss://eventsub-beta.wss.twitch.tv/ws",
# #     on_message = on_message,
# #     on_error = on_error,
# #     on_close = on_close)

# # ws.on_open = on_open
# # ws.run_forever()