import tweepy
import tweepy.asynchronous as twpy
from dotenv import dotenv_values

from test2 import on_tweet_received

config = dotenv_values(".env")
TWITTER_API_KEY = config.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = config.get("TWITTER_API_KEY_SECRET")
TWITTER_BEARER_TOKEN = config.get("TWITTER_BEARER_TOKEN")
TWITTER_ACCESS_TOKEN = config.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = config.get("TWITTER_ACCESS_TOKEN_SECRET")

client = twpy.AsyncClient(TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_ACCESS_TOKEN_SECRET, 
                     TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

class MyStreamingClient(twpy.AsyncStreamingClient):
    async def on_tweet(self, tweet):
        end_point = "https://twitter.com/twitter/status/"
        url = end_point + str(tweet.id)

stream_client = MyStreamingClient(TWITTER_BEARER_TOKEN)

# 清除之前套用的規則
print(stream_client.get_rules().data)
for rule in stream_client.get_rules().data:
    print(rule) 
    stream_client.delete_rules(rule.id)

# 新增規則
# 搜尋邏輯API： https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
stream_client.add_rules(tweepy.StreamRule(value="from:tooruche #小徹在攝攝 -is:retweet -is:reply"))
# 啟用
stream_client.filter()
