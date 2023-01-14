from twitchio.ext import commands, routines, eventsub
from twitchio import Channel, Client, HTTPException
from dotenv import dotenv_values
import random 
import json


config = dotenv_values("twitch-bot/env2")
TWITCH_ACCESS_TOKEN = config.get("TWITCH_ACCESS_TOKEN")
TWITCH_APP_SECRET = config.get("TWITCH_APP_SECRET")
CHANNEL_NAME = ["tooruche520"]


with open('twitch-bot/message_data.json', "r", encoding = "utf8") as file:
        data = json.load(file)

bot = commands.Bot(token=TWITCH_ACCESS_TOKEN, prefix='!', initial_channels=CHANNEL_NAME)
# eventsub_client = eventsub.EventSubClient(bot, TWITCH_APP_SECRET, "/callback", token=TWITCH_ACCESS_TOKEN)


@bot.event()
async def event_ready():
    
    print(f'Logged in as | {bot.nick}')
    print(f'User id is | {bot.user_id}')
    print(f'Connected channel is | {bot.connected_channels}')
    
    # bot.loop.create_task(eventsub_client.listen(port=4000))
    # try:
    #     await eventsub_client.subscribe_channel_follows(broadcaster="tooruche520")
    # except HTTPException:
    #     pass
    
    # 工作循環：發送輪播訊息
    @routines.routine(seconds=300)
    async def hi():
        message = random.choice(data)
        print(message)
        await bot.get_channel("tooruche520").send(f'{message}')
        
    hi.start()  
    
@bot.event()
async def event_eventsub_notification_follow(payload: eventsub.ChannelFollowData) -> None:
    print('Received event!')
    channel = bot.get_channel('tooruche520')
    await channel.send(f'{payload.data.user.name} followed woohoo!')

@bot.command()
async def hello(ctx: commands.Context):
    await ctx.send(f'Hello {ctx.author.name}!')
    print(f'Welcome')

bot.run()

# bot.loop.create_task(eventsub_client.listen(port=4000))
# bot.loop.create_task(bot.start())
# bot.loop.run_forever()