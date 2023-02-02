from src.Id_collection import emoji_list

def replace_emoji_dc(response):
    for emoji, emoji_id in emoji_list.items():
        response = response.replace(emoji, emoji_id)
    return response

def replace_emoji_tw(response):
    for emoji in emoji_list:
        response = response.replace(emoji, emoji[1:-1])
    return response


# d = replace_emoji_dc("username 多...摸摸我一點汪.. tc_is_husky")
# print(d)