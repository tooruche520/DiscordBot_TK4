import sqlite3
import logging as log
import datetime
import csv

TWITCH = "twitch"
DISCORD = "discord"

connect = sqlite3.connect('database/commands.db')
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
	"name"	TEXT,
    "count"  DECIMAL,
    "month"  TEXT,
    "platform"  TEXT,
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

def get_reply():
    commands_list = get_all_commands()
    result = {}
    for (id, name, response, brief, help, experience) in commands_list:
        result.setdefault(name, []).extend([response, brief, help, experience])
    return result   

def total_count(name, platform):
    command = f"SELECT SUM(COUNT) FROM usage_counter WHERE name='{name}' AND platform='{platform}'"
    return cursor_counter.execute(command).fetchone()[0]


def update_counter(name, time, platform):
    month_format = time.strftime('%Y-%m')
    
    command_check = f"SELECT * FROM usage_counter WHERE name='{name}' AND month='{month_format}' AND platform='{platform}'"
    command_add = f"INSERT INTO usage_counter(name, count, month, platform) VALUES ('{name}', 1, '{month_format}', '{platform}')"
    command_update = f"UPDATE usage_counter SET count=count+1 WHERE name='{name}' AND month='{month_format}' AND platform='{platform}'"

    if cursor_counter.execute(command_check).fetchall() == []:
        cursor_counter.execute(command_add)
    else:
        cursor_counter.execute(command_update)
        
    connect.commit()
    # print("Update counter")


def get_month_counter(month_format, platform):
    command_check = f"SELECT * FROM usage_counter WHERE month='{month_format}' AND platform='{platform}'"
    return cursor_counter.execute(command_check).fetchall()
    
def make_csv(month_format, platform):
    data = get_month_counter(month_format, platform)
    data.sort(key = lambda x: x[2], reverse=True)
    with open(f'每月指令統計表({platform}).csv', 'w', encoding="utf-8") as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['id', 'name', 'count', 'date', 'platform'])
        for row in data:
            csv_out.writerow(row)

    return True

# print(get_reply())
# update_counter('棒棒糖', datetime.datetime.today(), TWITCH)
# print(total_count("棒棒糖", TWITCH))
# update_counter('小頭', datetime.date(2023,12,19))
# update_counter('電烤爐', datetime.date(2023,4,19))
# update_counter('電烤爐', datetime.date(2023,1,19))
# update_counter('電烤爐', datetime.date(2023,1,19))
# data = get_month_counter("2023-01")
# make_csv("2023-01", TWITCH)
# print(dict(data))
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