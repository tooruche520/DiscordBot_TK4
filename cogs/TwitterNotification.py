import discord

import logging as log
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get
from src.Id_collection import channle_id, emoji_list, role_list
from dotenv import dotenv_values
import tweepy.asynchronous

config = dotenv_values(".env")
TWITTER_API_KEY = config.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = config.get("TWITTER_API_KEY_SECRET")
TWITTER_BEARER_TOKEN = config.get("TWITTER_BEARER_TOKEN")
TWITTER_ACCESS_TOKEN = config.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = config.get("TWITTER_ACCESS_TOKEN_SECRET")
CHANNLE_TWITTER_NOTIFICATION = channle_id["貼文通知"]

class TwitterNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        client = tweepy.Client(TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_ACCESS_TOKEN_SECRET, 
                     TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

        class MyStreamingClient(tweepy.asynchronous.AsyncStreamingClient):
            
            def set_dc_bot(self, bot):
                self.bot = bot
                
            async def on_tweet(self, tweet):
                end_point = "https://twitter.com/twitter/status/"
                url = end_point + str(tweet.id)
                log.info(f"Received tweet: {tweet.text}")
                channel = self.bot.get_channel(CHANNLE_TWITTER_NOTIFICATION)
                await channel.send(f"{url}")
                
            async def on_errors(self, errors):
                log.info(f"Received errors{errors}")
                

        # 清除之前套用的規則
        
        self.stream_client = MyStreamingClient(TWITTER_BEARER_TOKEN, wait_on_rate_limit=True)
    
            
    # event
    @commands.Cog.listener()
    async def on_ready(self):
        
        data = await self.stream_client.get_rules()
        if data[0] is not None:
            for rule in data[0]:
                await self.stream_client.delete_rules(rule.id)
        else :
            log.info("NO DATA")
        # 新增規則
        # 搜尋邏輯API： https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
        self.stream_client.set_dc_bot(self.bot)
        log.info("Finish setting twitter Notification.")
        await self.stream_client.add_rules(tweepy.StreamRule(value="from:tooruche #小徹在攝攝 -is:retweet -is:reply"))
        # 啟用
        await self.stream_client.filter()

        
    

# 要用 async await 
async def setup(bot):
    await bot.add_cog(TwitterNotification(bot))

# TK4-BOT測試
#小徹在攝攝