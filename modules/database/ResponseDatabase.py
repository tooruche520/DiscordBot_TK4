from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import timedelta
import pytz
from random import choice
from modules.EmojiReplace import replace_emoji

import logging as log

# 創建資料庫引擎，連接現有的資料庫
engine = create_engine('sqlite:///database/response.db')

# 宣告一個Base類，用來創建模型
Base = declarative_base()

# 定義Greeting模型（對應到資料庫中的Greeting表格）
class Greeting(Base):
    __tablename__ = 'Greeting'
    id = Column(Integer, primary_key=True)
    Command = Column(String)
    TimeStart = Column(Integer)
    TimeEnd = Column(Integer)
    Response = Column(String)

# 創建所有表格（如果表格已存在，這步會自動跳過）
Base.metadata.create_all(engine)

# 創建一個Session類，用來操作資料庫
Session = sessionmaker(bind=engine)
session = Session()


# 函數
# 打招呼回應 (!早安、!晚安)
async def get_greeting_response(ctx, command, send_time):
    # 定義台北時區
    tz_taipei = pytz.timezone('Asia/Taipei')

    # 取得台北時區的當前小時
    current_hour = send_time.astimezone(tz_taipei).hour
    
    # 查詢符合指令的回應
    greetings = session.query(Greeting).filter_by(Command=command).all()
    
    # 遍歷所有回應，找到符合時間區間的回應
    filtered_greetings = filter(lambda greeting: 
                                (greeting.TimeStart <= greeting.TimeEnd and
                                 greeting.TimeStart <= current_hour < greeting.TimeEnd) or
                                (greeting.TimeStart > greeting.TimeEnd and
                                 (greeting.TimeStart <= current_hour or current_hour < greeting.TimeEnd)),
                                greetings)
    
    appropriate_greetings = list(filtered_greetings)
    
    if appropriate_greetings:
        return await replace_emoji(ctx, choice(appropriate_greetings).Response)
    else:
        return "ERROR"