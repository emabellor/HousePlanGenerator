from FloorPlan.Room import RoomType, Room


class FloorPlan:
    def __init__(self):
        self.rooms = []

    def add_room(self, x, y, width, height, room_type: RoomType):
        self.rooms.append(Room(x, y, width, height, room_type))

    def merge_floor_plan(self, fp):
        self.merge_floor_plan_offset(fp, 0, 0)

    def merge_floor_plan_offset(self, fp, offset_x, offset_y):
        for r in fp.rooms:
            r.x += offset_x
            r.y += offset_y
            self.rooms.append(r)
