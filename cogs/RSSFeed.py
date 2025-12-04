import discord
from discord.ext import commands, tasks
from reader import make_reader
import os
import logging as log
from datetime import datetime
from google import genai
from dotenv import load_dotenv
load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

TEST_CHANNEL = 1028924185692618792

# --- 設定 ---
# 這裡定義每個 RSS Feed 的專屬設定 (額外資料)
# Key: RSS Feed URL
# Value: 該 Feed 的設定 (頻道 ID, 標籤名稱, 顏色, 圖示等)
FEED_CONFIG = {
    "https://bun.com/rss.xml": {
        "name": "Bun",
        "channel_id": TEST_CHANNEL, # 請修改為實際的頻道 ID
        "emoji": "<:bun:1445708292142792745>"
    },
    "https://nuxt.com/blog/rss.xml": {
        "name": "Nuxt",
        "channel_id": TEST_CHANNEL, # 請修改為實際的頻道 ID
        "emoji": "<:nuxt:1445708331694948453>"
    },
    "https://blog.vuejs.org/feed.rss": {
        "name": "Vue",
        "channel_id": TEST_CHANNEL, # 請修改為實際的頻道 ID
    },
    "https://blog.google/products/gemini/rss/": {
        "name": "Gemini",
        "channel_id": TEST_CHANNEL, # 請修改為實際的頻道 ID
    },
    "https://openai.com/news/rss.xml": {
        "name": "OpenAI",
        "channel_id": TEST_CHANNEL, # 請修改為實際的頻道 ID
    },
}

class RSSFeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # 確保 database 資料夾存在
        os.makedirs('database', exist_ok=True)
        
        # 初始化 reader，資料庫存放在 database/rss_data.db
        self.db_path = 'database/rss_data.db'
        self.reader = make_reader(self.db_path)
        
        # 初始化訂閱源
        self.init_feeds()
        
        # 啟動排程檢查
        self.check_rss.start()

    def init_feeds(self):
        """初始化：將設定中的 Feed 加入 reader (如果尚未加入)"""
        for url in FEED_CONFIG.keys():
            try:
                # 檢查是否已存在，不存在則加入
                if not self.reader.get_feed(url, None):
                    self.reader.add_feed(url)
                    log.info(f"[RSS] 已加入新訂閱: {url}")
            except Exception as e:
                log.error(f"[RSS] 加入訂閱失敗 {url}: {e}")

    def cog_unload(self):
        """Cog 卸載時停止排程"""
        self.check_rss.cancel()

    @tasks.loop(minutes=30)
    async def check_rss(self):
        """定期檢查 RSS 更新"""
        log.info("[RSS] 正在檢查 RSS 更新...")
        try:
            # 1. 更新所有訂閱源 (下載最新內容)
            self.reader.update_feeds()
            
            # 2. 針對每個訂閱源，只檢查最新的一筆
            for feed_url in FEED_CONFIG.keys():
                # 取得該 Feed 的最新一筆文章 (limit=1)
                entries = self.reader.get_entries(feed=feed_url, limit=1)
                entry = next(iter(entries), None)

                if not entry:
                    continue

                # 如果這篇文章已經讀過，就跳過
                if entry.read:
                    continue
                
                # 如果是未讀的，則發送
                config = FEED_CONFIG.get(feed_url)
                
                if not config:
                    self.reader.mark_entry_as_read(entry)
                    continue
                
                channel_id = config.get('channel_id')
                channel = self.bot.get_channel(channel_id)
                
                if channel:
                    await self.send_rss_message(channel, entry, config)
                else:
                    log.warning(f"[RSS] 找不到頻道 ID {channel_id} (Feed: {feed_url})")
                
                # 3. 標記為已讀
                self.reader.mark_entry_as_read(entry)
                
        except Exception as e:
            log.error(f"[RSS] 檢查更新時發生錯誤: {e}")

    async def send_rss_message(self, channel, entry, config):
        """發送 RSS 訊息到 Discord"""
        title = entry.title
        link = entry.link
        summary = entry.summary
        emoji = config.get('emoji', '')
        
        # 使用 Gemini 2.5 Pro 翻譯成繁體中文
        prompt = (
            f"請將以下文章摘要翻譯成繁體中文，並符合指定個格式。給我翻譯後的內容即可。\n\n"\
            f"以下是格式範例：\n"\
            f"## 測試標題\n"\
            f"測試摘要\n\n"\
            f"以下是文章內容：\n"\
            f"{title}\n{summary}"
        )
        
        translated_content = client.models.generate_content(
            model="gemini-2.5-flash-lite", contents=prompt
        ).text

        # 準備訊息內容
        translated_content = translated_content.replace('## ', f'## {emoji} ')
        content = f"{translated_content}\n{link}"

        try:
            await channel.send(content=content)
            log.info(f"[RSS] 已發送文章: {title} -> {channel.name}")
        except Exception as e:
            log.error(f"[RSS] 發送訊息失敗: {e}")

    @check_rss.before_loop
    async def before_check_rss(self):
        """等待 Bot 準備好再開始"""
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(RSSFeed(bot))
