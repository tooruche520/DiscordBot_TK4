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

TAG_NEW_FURRYPIC = "#小徹在攝攝"
TAG_NEW_INFO = "#T123"
TAG_FANART = "#T456"
TAG_FANART_R18 = "#T789"

client = tweepy.Client(TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_ACCESS_TOKEN_SECRET, 
                     TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

class MyStreamingClient(tweepy.asynchronous.AsyncStreamingClient):
    async def on_connect(self):
        log.info("Connected!")
    
    async def on_tweet(self, tweet):
        end_point = "https://twitter.com/twitter/status/"
        url = end_point + str(tweet.id)
        log.info(url)
        print(tweet)
        
        if TAG_NEW_FURRYPIC in tweet.text:
            self.on_new_pic(tweet)
        elif TAG_NEW_INFO in tweet.text:
            self.on_new_info(tweet)
        elif TAG_FANART in tweet.text:
            self.on_new_fanart(tweet)
        elif TAG_FANART_R18 in tweet.text:
            self.on_new_fanart_R18(tweet)
            
        # Test.on_tweet_callback(url)  
        # await asyncio.sleep(5)
    
    def on_new_pic(self, tweet):
        log.info("New PIC!!")
    
    def on_new_info(self, tweet):
        log.info("New INFO!!")
    
    def on_new_fanart(self, tweet):
        log.info("New FANART!!")
        # print(tweet)
        
    def on_new_fanart_R18(self, tweet):
        log.info("New R18 FANART!!")
        # print(tweet)
        
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
    rules = [
        tweepy.StreamRule(value=f"from:tooruche {TAG_NEW_FURRYPIC} -is:retweet -is:reply"),
        tweepy.StreamRule(value=f"from:tooruche {TAG_NEW_INFO} -is:retweet -is:reply"),
        tweepy.StreamRule(value=f"{TAG_FANART} -is:retweet -is:reply"),
        tweepy.StreamRule(value=f"{TAG_FANART_R18} -is:retweet -is:reply")
    ]
    # await stream_client.add_rules(tweepy.StreamRule(value="from:tooruche #小徹在攝攝 -is:retweet -is:reply"))
    # await stream_client.add_rules(tweepy.StreamRule(value="from:tooruche #AAAHHA -is:retweet -is:reply"))
    await stream_client.add_rules(add=rules)
    # 啟用
    await stream_client.filter()
    
asyncio.run(fun())
