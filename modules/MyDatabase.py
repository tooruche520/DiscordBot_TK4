import sqlite3
import logging as log
import modules.User as User
import csv
import asyncio
# from cogs.LevelSystem import send_level_up_message

# from modules.TK4_Logger import TK4_logger
# TK4_logger()

fp = open("src/level2exp.csv", "r", encoding="utf-8")
csv_reader = csv.reader(fp)
table_level_exp = list(csv_reader)
fp.close()

connect = sqlite3.connect('src/user_data/user.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS "user_exp" (
	"id"	INTEGER NOT NULL,
	"user_id"	TEXT,
	"adoption"	INTEGER,
	"level"	DECIMAL,
	"experience"	DECIMAL,
	PRIMARY KEY("id")
)""")

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

def update_user_exp(user_id, add_exp):
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
    log.debug(f"Successfully update user exp to database.")
    return is_upgrade

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
    experience = data[0][4]
    # print(user_id, adoption, level, experience)
    return User.User(user_id, adoption, level, experience)


