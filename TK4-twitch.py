from twitchio.ext import commands, routines, eventsub
from twitchio import Channel, Client, HTTPException
from dotenv import dotenv_values
import random 
import json
import modules.CommandsDatabase as command_db

config = dotenv_values(".env")
TWITCH_ACCESS_TOKEN = config.get("TWITCH_ACCESS_TOKEN")
TWITCH_APP_SECRET = config.get("TWITCH_APP_SECRET")
CHANNEL_NAME = ["tooruche520"]

with open('src/twitch_message_data.json', "r", encoding = "utf8") as file:
    data = json.load(file)

bot = commands.Bot(token=TWITCH_ACCESS_TOKEN, prefix='!', initial_channels=CHANNEL_NAME)
command_reply_dict = command_db.get_reply()


### Functions ###
    
def add_command_from_database():
    for name, info in command_reply_dict.items():
        @bot.command(name=name)
        async def fun(ctx):
            command_name = ctx.command.name
            command_db.update_counter(command_name, ctx.message.timestamp, command_db.TWITCH)
            response = command_reply_dict[command_name][0]
            total = command_db.total_count(command_name, command_db.TWITCH)
            response_n = response.replace("username", f'{ctx.author.name}').replace("total", str(total))
            await ctx.send(response_n)

@routines.routine(minutes=5)
async def message_loop():
    message = random.choice(data)
    print(message)
    await bot.get_channel("tooruche520").send(f'{message}')

def is_tootuche(func):
    async def decorator(ctx):
        if (ctx.author.name == 'tooruche520'):
            func(ctx)
        else:
            await ctx.send("如果你願意給我100跟棒棒糖，我就考慮幫你執行一下")

    return decorator

### Event ###

@bot.event()
async def event_ready():
    print(f'Logged in as | {bot.nick}')
    print(f'User id is | {bot.user_id}')
    print(f'Connected channel is | {bot.connected_channels}')
    add_command_from_database()
    
@bot.event()
async def event_message(message):
    if(message.echo):
        return 
    greeting_list = ["安安", "晚上好", "嗨"]
    if([greeting for greeting in greeting_list if(greeting in message.content)]):
        if(message.first):
            await message.channel.send(f"{message.author.name} 初見安安汪~")
        else:
            await message.channel.send(f"{message.author.name} 歡迎回到小徹攝影棚!")
    
### Commands ###

@bot.command()
async def start(ctx: commands.Context):
    @is_tootuche
    def run(ctx):
        message_loop.start()
    await run(ctx)
        

@bot.command()
async def cancel(ctx: commands.Context):
    @is_tootuche
    def run(ctx):
        message_loop.cancel()
    await run(ctx)
    await ctx.send("先休息一下汪uwuノ")
    
    
@bot.command()
async def link(ctx, link_name):
    command_db.update_counter("link", ctx.message.timestamp, command_db.TWITCH)
    links_map = {
        "github": "https://github.com/tooruche520/DiscordBot_TK4",
        "flickr": "https://www.flickr.com/people/tooruche520/",
        "discord": "https://discord.com/invite/HeywMdKNf5",
        "youtube": "https://www.youtube.com/@tooruche",
    }
    try:
        response = f"{link_name} 連結在此：{links_map[link_name.lower()]}"
    except KeyError:
        response = "好像輸入錯誤ㄌ，再檢查一下吧QQ"
    await ctx.send(response)
        

    
bot.run()

