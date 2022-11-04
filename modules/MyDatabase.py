import sqlite3
import User
connect = sqlite3.connect('src/user_data/test.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS "user_exp" (
	"id"	INTEGER NOT NULL,
	"user_id"	TEXT,
	"adoption"	TEXT,
	"level"	TEXT,
	"experience"	TEXT,
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

# TODO
def edit_user(user):
    command = "UPDATE user_exp "
    user_id = user.user_id
    adoption = user.adoption
    level = user.level
    experience = user.experience
    command += f"SET level='{level}' experience={experience});"
    cursor.execute(command)

# TODO
def delete_user(user):
    command = "INSERT INTO user_exp(user_id, adoption, level, experience) "
    user_id = user.user_id
    adoption = user.adoption
    level = user.level
    experience = user.experience
    value = f"VALUES('{user_id}', '{adoption}', {level}, {experience});"
    cursor.execute(command+value)

# TODO
def get_user(user):
    command = "INSERT INTO user_exp(user_id, adoption, level, experience) "
    user_id = user.user_id
    adoption = user.adoption
    level = user.level
    experience = user.experience
    value = f"VALUES('{user_id}', '{adoption}', {level}, {experience});"
    cursor.execute(command+value)


user = User.User('000123', 'twitch_sub', 1, 0)
add_user(user)
connect.commit()
connect.close()

# TODO: 重建資料庫的function，跟DC現有成員名單比對，若無則加入