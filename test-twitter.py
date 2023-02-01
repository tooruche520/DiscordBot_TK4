import tweepy.asynchronous
from dotenv import dotenv_values
# from test2 import BBB
from cogs.Test import Test
import asyncio
import logging as log
from modules.TK4_Logger import TK4_logger
TK4_logger()

config = dotenv_values(".env")
TWITTER_API_KEY = config.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = config.get("TWITTER_API_KEY_SECRET")
TWITTER_BEARER_TOKEN = config.get("TWITTER_BEARER_TOKEN")
TWITTER_ACCESS_TOKEN = config.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = config.get("TWITTER_ACCESS_TOKEN_SECRET")

client = tweepy.Client(TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_ACCESS_TOKEN_SECRET, 
                     TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

class MyStreamingClient(tweepy.asynchronous.AsyncStreamingClient):
    async def on_connect(self):
        log.info("Connected!")
    
    async def on_tweet(self, tweet):
        end_point = "https://twitter.com/twitter/status/"
        url = end_point + str(tweet.id)
        log.info(url)
        # Test.on_tweet_callback(url)  
        # await asyncio.sleep(5)

stream_client = MyStreamingClient(TWITTER_BEARER_TOKEN, wait_on_rate_limit=True)

async def fun():
    # 清除之前套用的規則
    data = await stream_client.get_rules()
    if data[0] is not None:
        log.info(data[0])
        for rule in data[0]:
            log.info(rule) 
            await stream_client.delete_rules(rule.id)
    else :
        log.info("NO DATA")

    # 新增規則
    # 搜尋邏輯API： https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    await stream_client.add_rules(tweepy.StreamRule(value="from:tooruche #小徹在攝攝 -is:retweet -is:reply"))
    # 啟用
    await stream_client.filter()
    
asyncio.run(fun())
