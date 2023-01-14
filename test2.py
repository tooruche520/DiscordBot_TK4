import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
TWITCH_APP_ID = config.get("TWITCH_APP_ID")
TWITCH_APP_SECRET = config.get("TWITCH_APP_SECRET")

body = {
    'client_id': TWITCH_APP_ID,
    'client_secret': TWITCH_APP_SECRET,
    "grant_type": 'client_credentials'
}

r = requests.post('https://id.twitch.tv/oauth2/token', body)
keys = r.json()
print(f'key= {keys}')

API_HEADERS = {
    'Client-ID': TWITCH_APP_ID,
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Authorization': 'Bearer ' + keys['access_token']
}

url = 'https://api.twitch.tv/helix/users?login=tooruche520'
req = requests.Session().get(url, headers=API_HEADERS)
jsondata = req.json()
print(jsondata)