import sqlite3
import logging as log
import csv
from enum import IntEnum, unique
from modules.LimitCounter import get_limit_count, add_count

fp = open("src/level2exp.csv", "r", encoding="utf-8")
csv_reader = csv.reader(fp)
table_level_exp = list(csv_reader)
fp.close()

connect = sqlite3.connect('database/user.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS "user_exp" (
	"id"	INTEGER NOT NULL,
	"user_id"	TEXT,
	"adoption"	INTEGER,
	"level"	DECIMAL,
	"experience"	DECIMAL,
    "twitch_id" TEXT,
	PRIMARY KEY("id")
)""")

class User:
    @unique
    class Adoption(IntEnum):
        GENERAL = 0
        CHANNEL_POINTS = 1
        BITS = 2
        SUBSCRIBE = 3
        VIP = 4    

    def __init__(self, user_id, adoption=Adoption.GENERAL, level=0, experience=0):
        self.user_id = user_id
        self.adoption = adoption
        self.level = level
        self.experience = experience
    

def add_user(user):
    user_id = user.user_id
    if(get_user_by_userid(user_id) != None):
        log.debug(f"Didn't add user: User is already in database.")
        return

    adoption = user.adoption
    level = 1
    experience = 0
    
    command = "INSERT INTO user_exp(user_id, adoption, level, experience) "
    command += f"VALUES('{user_id}', '{adoption}', {level}, {experience});"
    cursor.execute(command)
    connect.commit()
    log.debug(f"Successfully add user to database.")
    
def edit_user_twitch_account(user_id, twitch_id):
    command = f"UPDATE user_exp SET twitch_id='{twitch_id}' WHERE user_id='{user_id}'"
    cursor.execute(command)
    connect.commit()
    log.info(f"Edited user twitch account.")
    return True
    
def update_user_exp(user_id, add_exp):
    if(get_limit_count(user_id) >= 5):
        log.info(f"Command limit.")
        return False

    add_count(user_id)  # 增加每小時限制計數
    command = "UPDATE user_exp "
    user = get_user_by_userid(user_id)
    if(user == None):
        log.error(f"Cannot get user data from database.")
        return False

    experience = user.experience + add_exp
    level = user.level
    is_upgrade = False
    if(level != 51):
        if(experience >= int(table_level_exp[level+1][1])):
            level += 1
            is_upgrade = True

    command += f"SET level='{level}', experience='{experience}' WHERE user_id='{user_id}'"
    # print(command)
    cursor.execute(command)
    connect.commit()
    # log.info(f"Successfully add user:{user_id} {add_exp} exp to database.")
    return is_upgrade


def reload_user_exp(user_id):
    command = "UPDATE user_exp "
    user = get_user_by_userid(user_id)
    if(user == None):
        log.error(f"Cannot get user data from database.")
        return False

    experience = user.experience
    level = user.level
    for i in range(0, 51):
        if(experience >= int(table_level_exp[i+1][1])):
            level = i+1

    command += f"SET level='{level}' WHERE user_id='{user_id}'"
    # print(command)
    cursor.execute(command)
    connect.commit()
    # log.info(f"Successfully add user:{user_id} {add_exp} exp to database.")
    return False
    

##TODO
def delete_user(user):
    command = "INSERT INTO user_exp(user_id, adoption, level, experience) "
    user_id = user.user_id
    adoption = user.adoption
    level = user.level
    experience = user.experience
    value = f"VALUES('{user_id}', '{adoption}', {level}, {experience});"
    cursor.execute(command+value)
    connect.commit()


def get_user_by_userid(user_id):
    command = f"SELECT * FROM user_exp WHERE user_id='{user_id}'"
    cursor.execute(command)
    data = cursor.fetchall()

    if(data == []):
        return None

    user_id = data[0][1]
    adoption = data[0][2]
    level = data[0][3]
    experience = data[0][5]
    # print(user_id, adoption, level, experience)
    return User(user_id, adoption, level, experience)


# def update_user_exp_test(ctx, add_exp, send_level_up_message_test):
#     user = ctx.author
#     if(get_limit_count(user.id) >= 5):
#         log.info(f"Command limit.")
#         return False

#     add_count(user.id)  # 增加每小時限制計數
#     command = "UPDATE user_exp "
#     user_data = get_user_by_userid(user.id)
#     if(user_data == None):
#         log.error(f"Cannot get user data from database.")
#         return False

#     experience = user_data.experience + add_exp
#     level = user_data.level
#     is_upgrade = False
#     if(level != 51):
#         if(experience >= int(table_level_exp[level+1][1])):
#             level += 1
#             is_upgrade = True

#     command += f"SET level='{level}', experience='{experience}' WHERE user_id='{user.id}'"
#     # print(command)
#     cursor.execute(command)
#     connect.commit()
#     asyncio.run(send_level_up_message_test(ctx, is_upgrade, level, user))
