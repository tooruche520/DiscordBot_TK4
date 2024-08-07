import modules.database.IdCollectionDatabase as ID

def replace_emoji_dc(response):
    # 將取得的DB資料轉換成dict格式
    emoji_data = ID.get_emoji_data()
    emoji_list = {emoji: emoji_id for emoji, emoji_id in emoji_data}
    
    for emoji, emoji_id in emoji_list.items():
        response = response.replace(emoji, emoji_id)
    return response

def replace_emoji_tw(response):
    # 將取得的DB資料轉換成dict格式
    emoji_data = ID.get_emoji_data()
    emoji_list = {emoji: emoji_id for emoji, emoji_id in emoji_data}
    
    for emoji in emoji_list:
        response = response.replace(emoji, emoji[1:-1])
    return response
