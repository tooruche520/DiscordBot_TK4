import json
import logging as log

def get_limit_count(user_id):
    user_id = str(user_id)
    with open('database/command_count.json', "r", encoding = "utf8") as file:
        data = json.load(file)
        if user_id not in data:
            return 0
        # log.info(f'get count {data[user_id]}')
        return data[user_id] 


def add_count(user_id):
    user_id = str(user_id)
    with open('database/command_count.json', "r", encoding = "utf8") as file:
        data = json.load(file)
        if user_id not in data:
            data[user_id] = 0
        elif data[user_id] >= 5:
            return 
        data[user_id] += 1

    with open('database/command_count.json', "w", encoding = "utf8") as file:
        json.dump(data, file)

    # log.info(f'Successfully add count')

def clear():
    with open('database/command_count.json', "r", encoding = "utf8") as file:
        data = json.load(file)
        data = {}

    with open('database/command_count.json', "w", encoding = "utf8") as file:
        json.dump(data, file)

    log.info(f'Successfully clear count')

def sub_count(user_id):
    user_id = str(user_id)
    with open('database/command_count.json', "r", encoding = "utf8") as file:
        data = json.load(file)
        if user_id not in data:
            data[user_id] = 0
        data[user_id] -= 1

    with open('database/command_count.json', "w", encoding = "utf8") as file:
        json.dump(data, file)