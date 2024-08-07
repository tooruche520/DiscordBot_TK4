import sqlite3

database_path = "database/idcollection.db"

def get_one_result(sql_command):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(sql_command)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def get_channel_id(channel_name):
    result = get_one_result(f"SELECT ChannelID FROM Channel WHERE ChannelName='{channel_name}'")
    return result

def get_emoji_id(emoji_name):
    result = get_one_result(f"SELECT EmojiID FROM Emoji WHERE EmojiName='{emoji_name}'")
    return result

def get_message_id(message_name):
    result = get_one_result(f"SELECT MessageID FROM Message WHERE MessageName='{message_name}'")
    return result

def get_role_id(role_name):
    result = get_one_result(f"SELECT RoleID FROM Role WHERE RoleName='{role_name}'")
    return result

def get_emoji_data():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Emoji')
    emoji_data = cursor.fetchall()
    conn.close()
    return emoji_data

def add_emoji(emoji_name, emoji_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    command = f"INSERT INTO Emoji (EmojiName, EmojiID) VALUES ('{emoji_name}', '{emoji_id}')"
    cursor.execute(command)
    conn.commit()
    conn.close()

def edit_emoji(before_emoji_name, after_emoji_name, after_emoji_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    command = f"UPDATE Emoji SET EmojiName = '{after_emoji_name}', EmojiID = '{after_emoji_id}' WHERE EmojiName = '{before_emoji_name}'"
    cursor.execute(command)
    conn.commit()
    conn.close()

def delete_emoji(emoji_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    command = f"DELETE FROM Emoji WHERE EmojiID = '{emoji_id}'"
    cursor.execute(command)
    conn.commit()
    conn.close()