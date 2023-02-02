from enum import IntEnum, unique

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
    

