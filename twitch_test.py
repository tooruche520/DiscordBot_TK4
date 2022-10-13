from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get
import discord
import json
import requests
import logging as log

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)


with open('token.json', "r", encoding = "utf8") as file:
    data = json.load(file)
    APP_ID = data['TWITCH_APP_ID']
    APP_SECRET = data['TWITCH_APP_SECRET']
    DISCORD_BOT_TOKEN = data['DISCORD_BOT_TOKEN']

with open('data.json', "r", encoding = "utf8") as file:
    data = json.load(file)
    my_channel_ID = data['TK4開發測試頻道']
    role_twitch = data['role_list']['優質圖奇觀眾']

body = {
    'client_id': APP_ID,
    'client_secret': APP_SECRET,
    "grant_type": 'client_credentials'
}

r = requests.post('https://id.twitch.tv/oauth2/token', body)
keys = r.json()
# print(f'key= {keys}')

# Authentication with Twitch API.
twitch = Twitch(APP_ID, APP_SECRET)
twitch.authenticate_app([])
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams?{}"
API_HEADERS = {
    'Client-ID': APP_ID,
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Authorization': 'Bearer ' + keys['access_token']
}

# print(twitch.get_users(logins=["williamhuang0520"]))

# Returns true if online, false if not.
def checkuser(user):
    try:
        url = TWITCH_STREAM_API_ENDPOINT_V5.format(f"user_login={user}")
        try:
            req = requests.Session().get(url, headers=API_HEADERS)
            jsondata = req.json()
            # print(jsondata)
            for info in jsondata['data']:
                # print(f'{info["user_name"]} is streaming!')
                return True, jsondata
            else:
                # print(f'{user} is not streaming!')
                return False, None    
        except Exception as e:
            print("Error checking user: ", e)
            return False, None
    except IndexError:
        return False, None

# print(checkuser('dolphinshine'))
# print(checkuser('capybara_arumao'))
# print(checkuser('shuteye_orange'))

# testBool, testJson = checkuser('dolphinshine')
# print(testBool, testJson)


# tooruche520: 790529577
# williamhuang0520: 836535586
# shuteye_orange: 39755984663


twitch_name = 'williamhuang0520'
last_started_at = '2022-10-12T02:38:03Z'

# Executes when bot is started
@bot.event
async def on_ready():
    @tasks.loop(seconds=10)
    async def live_notifs_loop():
        guild = bot.get_guild(1028268840112640100)
        role = guild.get_role(int(role_twitch))
        channel = bot.get_channel(int(my_channel_ID))

        status, response = checkuser(twitch_name)

        global last_started_at
        if status is True :
            current_start_time = response["data"][0]["started_at"]
            if current_start_time != last_started_at:
                last_started_at = current_start_time
                await channel.send(
                    f"{role.mention}\n{twitch_name} 現在正在直播! 快來看看吧!"
                    f"\nhttps://www.twitch.tv/{twitch_name}")
                log.info(f"{twitch_name} started streaming. Sending a notification.")

    live_notifs_loop.start()

print('Server Running')
bot.run(DISCORD_BOT_TOKEN)