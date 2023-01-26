import sqlite3
import logging as log
import datetime
# import modules.User as User
import csv
# from modules.LimitCounter import get_limit_count, add_count

# fp = open("src/level2exp.csv", "r", encoding="utf-8")
# csv_reader = csv.reader(fp)
# table_level_exp = list(csv_reader)
# fp.close()

connect = sqlite3.connect('src/database/commands.db')
cursor_commands = connect.cursor()
cursor_counter = connect.cursor()

cursor_commands.execute("""CREATE TABLE IF NOT EXISTS "commands" (
	"id"    INTEGER NOT NULL,
	"name"	TEXT,
	"response"	TEXT,
	"brief"	TEXT,
	"help"  TEXT,
	"experience"  DECIMAL,
	PRIMARY KEY("id")
)""")

cursor_counter.execute("""CREATE TABLE IF NOT EXISTS "usage_counter" (
    "id"    INTEGER NOT NULL,
    "month"  TEXT,
	"name"	TEXT,
    "count"  DECIMAL,
	PRIMARY KEY("id")
)""")

def add_command(name, response, brief, help, experience):
    command = "INSERT INTO commands(name, response, brief, help, experience) "
    command += f"VALUES('{name}', '{response}', '{brief}', '{help}', {experience});"
    cursor_commands.execute(command)
    connect.commit()
    log.debug(f"Successfully add command to database.")

def get_all_commands():
    command = f"SELECT * FROM commands"
    cursor_commands.execute(command)
    commands_list = cursor_commands.fetchall()

    if(commands_list == []):
        return None

    return commands_list

# [DEBUG]
def update_counter(name, time):
    month_formate = time.strftime('%Y-%m')
    
    command_check = f"SELECT * FROM usage_counter WHERE name='{name}' AND month='{month_formate}'"
    command_add = f"INSERT INTO usage_counter(month, name, count) VALUES ('{month_formate}', '{name}', 1)"
    command_update = f"UPDATE usage_counter SET count=count+1 WHERE name='{name}' AND month='{month_formate}'"

    if cursor_counter.execute(command_check).fetchall() == []:
        cursor_counter.execute(command_add)
    else:
        cursor_counter.execute(command_update)
        
    connect.commit()
    print("Update counter")

# [DEBUG]
def get_month_counter(month_formate):
    command_check = f"SELECT * FROM usage_counter WHERE month='{month_formate}'"
    return cursor_counter.execute(command_check).fetchall()
    
    
# update_counter('小頭', datetime.datetime.today())
# update_counter('小頭', datetime.date(2023,12,19))
# update_counter('電烤爐', datetime.date(2023,4,19))
# update_counter('電烤爐', datetime.date(2023,1,19))
# update_counter('電烤爐', datetime.date(2023,1,19))
# print(get_month_counter("2023-01"))
# update_counter('電烤爐')
# update_counter('電烤爐')
# update_counter('電烤爐')
# update_counter('電烤爐')



# add_command("小頭", "今晚來小徹的辦公室", "催小徹發薪水", "!電烤爐\n讓小徹成爲您的電烤爐，請不要用金屬夾去夾肉哦", 5)
# add_command("電烤爐", "請記得不要用金屬夾去夾肉哦", "小徹負責當電烤爐", "!小頭\n讓小徹儘快出薪水", 5)
# commands_list = get_all_commands()
# for command in commands_list:
#     name = command[1]
#     response = command[2]
#     brief = command[3]
#     help = command[4]
#     experience = command[5]
#     print(name, response, brief, help, experience)
#     print(command)