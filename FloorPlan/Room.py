from enum import Enum


class RoomType(Enum):
    LIVING_ROOM = 1
    BEDROOM = 2,
    KITCHEN = 3,
    BATHROOM = 4,
    EXTRA_ROOM = 5


class Room:
    def __init__(self, x, y, width, height, room_type: RoomType):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room_type = room_type

