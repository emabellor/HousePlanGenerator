from FloorPlan.Room import RoomType, Room
from typing import List


class FloorPlan:
    def __init__(self, width, height):
        self.rooms:List[Room] = []
        self.width = width
        self.height = height
        self.name = ''
        self.length = 9

    def add_room(self, x, y, width, height, room_type: RoomType):
        self.rooms.append(Room(x, y, width, height, room_type))

    def merge_floor_plan(self, fp):
        self.merge_floor_plan_offset(fp, 0, 0)

    def merge_floor_plan_offset(self, fp, offset_x, offset_y):
        for r in fp.rooms:
            r.x += offset_x
            r.y += offset_y
            self.rooms.append(r)
