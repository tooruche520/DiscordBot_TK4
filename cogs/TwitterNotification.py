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
CHANNLE_PHOTOGRAPHY_GALLERY = channle_id["攝影作品"]
CHANNLE_TWITTER_NOTIFICATION = channle_id["貼文通知"]
CHANNEL_FANART = channle_id["小徹粉絲繪"]
CHANNEL_FANART_R18 = channle_id["小徹色圖"]

TAG_NEW_FURRYPIC = "#小徹在攝攝"
TAG_NEW_INFO = "#公告"
TAG_FANART = "#小徹在發電"
TAG_FANART_R18 = "#小徹在漏電"

class TwitterNotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stream_client = MyStreamingClient(TWITTER_BEARER_TOKEN, wait_on_rate_limit=True)
        self.channel_photography_gallery = bot.get_channel(CHANNLE_PHOTOGRAPHY_GALLERY)
        self.channel_twitter_notifaction = bot.get_channel(CHANNLE_TWITTER_NOTIFICATION)
        self.channel_fanart = bot.get_channel(CHANNEL_FANART)
        self.channel_fanart_r18 = bot.get_channel(CHANNEL_FANART_R18)
        
    def add_self(self, instance):
        self.instance = instance
            
    # event
    @commands.Cog.listener()
    async def on_ready(self):
        await self.stream_client.add_instance(self.instance)
        data = await self.stream_client.get_rules()
        if data[0] is not None:
            log.info(data[0])
            for rule in data[0]:
                log.info(rule) 
                await self.stream_client.delete_rules(rule.id)
        else :
            log.info("NO DATA")

        # 新增規則
        # 搜尋邏輯API： https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
        rules = [
            tweepy.StreamRule(value=f"from:tooruche {TAG_NEW_FURRYPIC} -is:retweet -is:reply"),
            tweepy.StreamRule(value=f"from:tooruche {TAG_NEW_INFO} -is:retweet -is:reply"),
            tweepy.StreamRule(value=f"{TAG_FANART} -is:retweet -is:reply"),
            tweepy.StreamRule(value=f"{TAG_FANART_R18} -is:retweet -is:reply")
        ]
        
        await self.stream_client.add_rules(add=rules)
        await self.stream_client.filter()

    async def on_new_pic(self, tweet):
        url = MyStreamingClient.to_url(tweet)
        response = f"小徹發新毛毛照了，快去點讚{emoji_list[':tc_happy:']}\n{url}"
        await self.bot.get_channel(CHANNLE_PHOTOGRAPHY_GALLERY).send(response)
        log.info("New PIC!!")
    
    async def on_new_info(self, tweet):
        url = MyStreamingClient.to_url(tweet)
        response = f"小徹發新公告了，快去看看{emoji_list[':tc_tongue:']}\n{url}"
        await self.bot.get_channel(CHANNLE_TWITTER_NOTIFICATION).send(response)
        log.info("New INFO!!")
    
    async def on_new_fanart(self, tweet):
        url = MyStreamingClient.to_url(tweet)
        response = f"小徹有新的粉絲繪了，好棒!!!{emoji_list[':tc_is_husky:']}\n{url}"
        await self.bot.get_channel(CHANNEL_FANART).send(response)
        log.info("New FANART!!")
        
    async def on_new_fanart_R18(self, tweet):
        url = MyStreamingClient.to_url(tweet)
        response = f"小徹有新的瑟圖了，好瑟好香ㄛ{emoji_list[':tc_sip2:']}\n{url}"
        await self.bot.get_channel(CHANNEL_FANART_R18).send(response)
        log.info("New R18 FANART!!")
        
    

# 要用 async await 
async def setup(bot):
    instance = TwitterNotification(bot)
    await bot.add_cog(instance)
    instance.add_self(instance)

# TK4-BOT測試
#小徹在攝攝

class MyStreamingClient(tweepy.asynchronous.AsyncStreamingClient):
    
    async def add_instance(self, instance):
        self.instance = instance
    
    async def on_connect(self):
        log.info("Connected!")
    
    async def on_tweet(self, tweet):
        end_point = "https://twitter.com/twitter/status/"
        url = end_point + str(tweet.id)
        log.info(url)
        print(tweet)
        
        if TAG_NEW_FURRYPIC in tweet.text:
            await TwitterNotification.on_new_pic(self.instance, tweet)
        elif TAG_NEW_INFO in tweet.text:
            await TwitterNotification.on_new_info(self.instance, tweet)
        elif TAG_FANART in tweet.text:
            await TwitterNotification.on_new_fanart(self.instance, tweet)
        elif TAG_FANART_R18 in tweet.text:
            await TwitterNotification.on_new_fanart_R18(self.instance, tweet)
            
        # Test.on_tweet_callback(url)  
        # await asyncio.sleep(5)
    
    def to_url(tweet):
        end_point = "https://twitter.com/twitter/status/"
        url = end_point + str(tweet.id)
        return url
    
    # def on_new_pic(self, tweet):
    #     log.info("New PIC!!")
    
    # def on_new_info(self, tweet):
    #     log.info("New INFO!!")
    
    # def on_new_fanart(self, tweet):
    #     log.info("New FANART!!")
    #     # print(tweet)
        
    # def on_new_fanart_R18(self, tweet):
    #     log.info("New R18 FANART!!")
    #     # print(tweet)
  