import sqlite3
import logging as log

connect = sqlite3.connect('database/gameinfo.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS "games" (
	"id"    INTEGER NOT NULL,
	"name"	TEXT,
	"newest_title"	TEXT,
	PRIMARY KEY("id")
)""")

def get_newest_title(game_name):
    command = f"SELECT newest_title FROM games where name='{game_name}'"
    cursor.execute(command)
    connect.commit()
    data = cursor.fetchall()
    return data[0][0]

def update_newest_title(game_name, newest_title):
    command = f"UPDATE games SET newest_title='{newest_title}' WHERE name='{game_name}'"
    cursor.execute(command)
    connect.commit()
    



# print(get_newest_title("pokemon_sv"))
# update_newest_title("pokemon_sv", "サーフゴーの育成論と対策 を公開")