import sqlite3
import logging as log
import User

connect = sqlite3.connect('src/user_data/test.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS "user_exp" (
	"id"	INTEGER NOT NULL,
	"user_id"	TEXT,
	"adoption"	TEXT,
	"level"	DECIMAL,
	"experience"	DECIMAL,
	PRIMARY KEY("id")
)""")

def add_user(user):
    command = "INSERT INTO user_exp(user_id, adoption, level, experience) "
    user_id = user.user_id
    adoption = user.adoption
    level = 0
    experience = 0
    command += f"VALUES('{user_id}', '{adoption}', {level}, {experience});"
    cursor.execute(command)
    connect.commit()
    log.debug(f"Successfully add user to database.")

def update_user_exp(user_id, add_exp):
    command = "UPDATE user_exp "
    user = get_user_by_userid(user_id)
    # user_id = user.user_id
    # adoption = user.adoption
    experience = user.experience + add_exp
    level = user.level ##TODO
    # print(experience, level)
    command += f"SET level='{level}', experience='{experience}' WHERE user_id='{user_id}'"
    # print(command)
    cursor.execute(command)
    connect.commit()
    log.debug(f"Successfully update user exp to database.")

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

##TODO
def get_user_by_userid(user_id):
    command = f"SELECT * FROM user_exp WHERE user_id='{user_id}'"
    cursor.execute(command)
    data = cursor.fetchall()

    user_id = data[0][1]
    adoption = data[0][2]
    level = data[0][3]
    experience = data[0][4]
    # print(user_id, adoption, level, experience)
    return User.User(user_id, adoption, level, experience)


user = User.User('000123', 'twitch_sub', 99, 999)
# add_user(user)
# add_user(User.User('000124', 'twitch_sub', 6, 36))
# add_user(User.User('000125', 'twitch_sub', 7, 57))
# add_user(User.User('000126', 'twitch_sub', 8, 77))
# add_user(User.User('000127', 'twitch_sub', 8, 97))
# update_user(user)
# print(get_user_by_userid('000127').user_id)
update_user_exp('000127', 98999)
connect.commit()
connect.close()

# TODO: 重建資料庫的function，跟DC現有成員名單比對，若無則加入