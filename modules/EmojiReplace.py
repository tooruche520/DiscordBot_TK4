import re
import discord
from discord.ext import commands
import logging as log

import modules.database.IdCollectionDatabase as ID

async def replace_emoji(ctx, message):
    emoji_pattern = r':\w+:'
    matches = re.findall(emoji_pattern, message)
    
    for match in matches:
        try:
            # 嘗試將表情符號名稱轉換成 Emoji 物件
            emoji = await commands.EmojiConverter().convert(ctx, match.strip(":"))
            # 將字串中的表情符號名稱替換成對應的表情符號
            message = message.replace(match, str(emoji))
        except commands.CommandError:
            # 如果轉換失敗，跳過該表情符號
            continue
    
    return message

def replace_emoji_tw(response):
    # 將取得的DB資料轉換成dict格式
    emoji_data = ID.get_emoji_data()
    emoji_list = {emoji: emoji_id for emoji, emoji_id in emoji_data}
    
    for emoji in emoji_list:
        response = response.replace(emoji, emoji[1:-1])
    return response
