from random import randint
from src.Id_collection import emoji_list

morning_data = {
    'h0-6': 
    [
        "現在說早安是不是有點早啊...????" + emoji_list['tc_tongue'], 
        "嗷夜對身體不太好喔OAO" + emoji_list['tc_sad'], 
        "早安...（哈欠 + ",
        "半夜還早安，小壞壞。你怎麼這麼早起床呢? 是不是被夢想中的美味骨頭吵醒了?"
    ],
    'h6-12': 
    [   
        "早安早早安~今天也是充滿活力的一天!!" + emoji_list['tc_happy'], 
        "起的真早呀嗷~" + emoji_list['tc_tongue'], 
        "早安~每天好心情，凡事皆如意（遞荷花"
    ],
    'h12-18': 
    [
        "你好像睡得有點久喔ww" + emoji_list['tc_angry'],
        "要一起吃午晚餐咪?" + emoji_list['tc_tongue'],
        "看看你的屁屁 太陽公公把他烤得金黃酥脆了" + emoji_list['tc_tongue']
    ],
    'h18-24': 
    [
        "美國的朋友早安呀~" + emoji_list['tc_happy'],
        "你的時間是錯位了咪?" + emoji_list['tc_tongue'],
        "你在發什咪神經"
    ],
    '南極':
    [
        "聽說南極現在是永晝 說早安沒問題吧 a8 "
          
    ]
}

def morning_response(send_time):
    hour = send_time.hour
    if 0 <= hour and hour < 6:
        return morning_data['h0-6'][randint(0, 3)]
    elif 6 <= hour and hour < 12:
        return morning_data['h6-12'][randint(0, 2)]
    elif 12 <= hour and hour < 18:
        return morning_data['h12-18'][randint(0, 2)]
    elif 18 <= hour and hour < 24:
        return morning_data['h18-24'][randint(0, 2)]
    else:
        return "ERROR"

night_data = {
    'h1-6': 
    [
        "晚安晚安汪(*´∀`)~♥", 
        "嗷夜對身體不太好喔OAO" + emoji_list['tc_sad'], 
        "我...我還能撐" + emoji_list['tc_sad']
    ],
    'h6-12': 
    [   
        "嗷夜奮戰辛苦了，要來個睡前抱抱嗎?祝你好夢!" + emoji_list['tc_happy'], 
        "好亮!這樣你睡得著咪", 
        "不可以翹課喔~等一下都是空堂對吧!" + emoji_list['tc_sad'], 
    ],
    'h12-18': 
    [
        "晚安，朋友，早安，要睡懶覺嗎" + emoji_list['tc_tongue'],
        "要一起吃消夜咪?" + emoji_list['tc_is_husky'],
        "你在發什咪神經" + emoji_list['tc_angry']
    ],
    'h18-21': 
    [
        "今天很早睡ㄛ 身體健康 萬事如意",
        "你的時間是錯位了咪?",
        "上班上課累壞了咪?那就先好好休息吧" + emoji_list['tc_tongue']
    ],
    'h21-1': 
    [
        "晚安晚安汪(*´∀`)~♥",
        "明天早上起床也是活力滿滿的一天!" + emoji_list['tc_happy'],
        "祝你夢到毛茸茸天堂!" + emoji_list['tc_happy'],
        "晚安，記得睡前充足電量喔"
    ],
    '南極':
    [
        "聽說南極現在是永夜 說晚安沒問題吧 a8 "
        
    ]
}


def night_response(send_time):
    hour = send_time.hour
    if 1 <= hour and hour < 6:
        return night_data['h1-6'][randint(0, 2)]
    elif 6 <= hour and hour < 12:
        return night_data['h6-12'][randint(0, 2)]
    elif 12 <= hour and hour < 18:
        return night_data['h12-18'][randint(0, 2)]
    elif 18 <= hour and hour < 21:
        return night_data['h18-21'][randint(0, 2)]
    else:
        return night_data['h21-1'][randint(0, 3)]