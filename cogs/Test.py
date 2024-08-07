from discord.ext import commands, tasks
import logging as log
import modules.database.UserDatabase as db
import modules.database.IdCollectionDatabase as ID
from cogs.LevelSystem import LevelSystem
import modules.database.CommandsDatabase as command_db
import asyncio

# | 指令       | 描述                    | 經驗值             | 備註                    |
# | ---------- | ----------------------- | ------------------ | ----------------------- |
# | !棒棒糖    | 餵 TK4 一根棒棒糖       | 增加 {N}           |                         |
# | !晚安      | 跟 TK4 說晚安           | 增加 {N}           |                         |
# | !尖頭拉瑞  | 對 TK4 說尖頭拉瑞       | **經驗值不會增加** | 小徹不開心，TK4也不開心 |
# | !吃 \*食物 | 讓 TK4 幫忙送食物給小徹 | 看你給什麼         | 給喜歡的可能會加比較多  |
# | 以下待加入 | ----------------------- | ------------------ | ----------------------- |
# | !rua       | 摸摸TK4 uwu             | 增加 {N}           |                         |

ROLE_HUSKY = ID.get_role_id("偉大的哈士奇總裁")

class Test(commands.Cog, description="測試用的類別"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(1028268840112640100)
        guild_emojis = guild.emojis
        
        database_emojis = ID.get_emoji_data()
        
        # 將資料庫中的emoji轉換為字典，方便查找
        database_emoji_dict = {emoji[0]: emoji[1] for emoji in database_emojis}

        for emoji in guild_emojis:
            emoji_name = f':{emoji.name}:'
            emoji_id = str(emoji)

            if emoji_name not in database_emoji_dict:
                ID.add_emoji(emoji_name, emoji_id)
                log.info(f"新增表符成功 {emoji_name} ({emoji_id})")
            # else:
            #     log.info(f"Emoji {emoji_name} already exists in the database.")
        
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        before_emojis = set(before)
        after_emojis = set(after)

        # Determine added and removed emojis
        added = after_emojis - before_emojis
        removed = before_emojis - after_emojis

        if added:
            for emoji in added:
                ID.add_emoji(f':{emoji.name}:', str(emoji))
                log.info(f"新增表符成功 :{emoji.name}: ({emoji})")
        if removed:
            for emoji in removed:
                ID.delete_emoji(str(emoji))
                log.info(f"刪除表符成功 :{emoji.name}: ({emoji})")

        # Determine modified emojis
        for emoji in after_emojis & before_emojis:
            before_emoji = next(e for e in before if e.id == emoji.id)
            after_emoji = next(e for e in after if e.id == emoji.id)
            if before_emoji.name != after_emoji.name:
                ID.edit_emoji(f':{before_emoji.name}:', f':{after_emoji.name}:', str(after_emoji))
                log.info(f"表符名稱變更 :{before_emoji.name}: -> :{after_emoji.name}: ({before_emoji} -> {after_emoji})")
            

    
           
# 要用 async await 
async def setup(bot):
    await bot.add_cog(Test(bot))
