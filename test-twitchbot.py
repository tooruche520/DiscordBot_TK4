from twitchio.ext import commands
from twitchio import Channel
from dotenv import dotenv_values

config = dotenv_values("env2")
TWITCH_ACCESS_TOKEN = config.get("TWITCH_ACCESS_TOKEN")
CHANNEL_NAME = ["tooruche520"]

bot = commands.Bot(token=TWITCH_ACCESS_TOKEN, prefix='!', initial_channels=CHANNEL_NAME)
# channel = Channel(name=CHANNEL_NAME)


@bot.event()
async def event_ready():
    # Notify us when everything is ready!
    # We are logged in and ready to chat and use commands...
    print(f'Logged in as | {bot.nick}')
    print(f'User id is | {bot.user_id}')
    print(f'Connected channel is | {bot.connected_channels}')
    
@bot.command()
async def hello(ctx: commands.Context):
    await ctx.send(f'Hello {ctx.author.name}!')
    print(f'Welcome')
    

    
bot.run()