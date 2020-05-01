from Constraints.ConstraintSet2 import ConstraintSet
from Constraints.MinMax import MinMax
from FloorPlan.Room import RoomType, Room
from FloorPlan.RoomNode import RoomNode


class SuburbanGenerator:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.constraints = ConstraintSet()
        self.constraints.add_or_update('LivingRooms', MinMax(1, 1))
        self.constraints.add_or_update('AreaLivingRooms', MinMax(400, 500))

        self.constraints.add_or_update('BedRooms', MinMax(1, 2))
        self.constraints.add_or_update('AreaBedRooms', MinMax(400, 500))

        self.constraints.add_or_update('Bathrooms', MinMax(0, 1))
        self.constraints.add_or_update('AreaBathrooms', MinMax(200, 200))

        self.constraints.add_or_update('Kitchens', MinMax(0, 1))
        self.constraints.add_or_update('AreaKitchens', MinMax(200, 200))

        self.constraints.add_or_update('ExtraRoom', MinMax(0, 1))
        self.constraints.add_or_update('AreaCloset', MinMax(100, 100))

    def set_static_room_number(self, room_type: RoomType, rooms: int):
        if rooms < 0:
            raise Exception('Room number cannot be zero')

        if room_type == RoomType.EXTRA_ROOM and rooms > 1:
            raise Exception('Rooms cant be greater than 1 for EXTRA_ROOM type')

        room_name_constraint = self.get_room_name_constraint(room_type)
        constraint =  MinMax(rooms, rooms)
        self.constraints.add_or_update(room_name_constraint, constraint)

    @staticmethod
    def get_room_name_constraint(room_type: RoomType):
        if room_type == RoomType.KITCHEN:
            return 'Kitchens'
        elif room_type == RoomType.BATHROOM:
            return 'Bathrooms'
        elif room_type == RoomType.BEDROOM:
            return 'BedRooms'
        elif room_type == RoomType.LIVING_ROOM:
            return 'LivingRooms'
        elif room_type == RoomType.EXTRA_ROOM:
            return 'ExtraRoom'
        else:
            raise Exception('Type not recognized: ' + room_type.name)

    def generate_floor_plan(self):
        main: RoomNode = None

        living_rooms = self.constraints.generate_value('LivingRooms')
        bedrooms = self.constraints.generate_value('BedRooms')
        bathrooms = self.constraints.generate_value('Bathrooms')
        kitchens = self.constraints.generate_value('Kitchens')

        print('Total living rooms: ', living_rooms)
        print('Total bedrooms: ', bedrooms)
        print('Total bathrooms: ', bathrooms)
        print('Total kitchens: ', kitchens)

        # Generate living rooms
        for i in range(living_rooms):
            if main is None:
                main = self.generate_valid_room(RoomType.LIVING_ROOM)
            else:
                main.children.insert(0, self.generate_valid_room(RoomType.LIVING_ROOM))

        # Generate bedrooms
        for i in range(bedrooms):
            if main is None:
                main = self.generate_valid_room(RoomType.BEDROOM)
            else:
                main.children.insert(0, self.generate_valid_room(RoomType.BEDROOM))

        # Generate Bathrooms
        for i in range(bathrooms):
            if main is None:
                main = self.generate_valid_room(RoomType.BATHROOM)
            else:
                main.children.insert(0, self.generate_valid_room(RoomType.BATHROOM))

        # Generate Kitchen
        for i in range(kitchens):
            if main is None:
                main = self.generate_valid_room(RoomType.KITCHEN)
            else:
                main.children.insert(0, self.generate_valid_room(RoomType.KITCHEN))

        if main is None:
            raise Exception('There is not rooms to draw in the floor plan')
        else:
            return main.to_floor_plan_width_height(self.width, self.height)

    def generate_valid_room(self, room_type:RoomType):
        room = RoomNode(room_type)

        if room_type == RoomType.LIVING_ROOM:
            room.area = self.constraints.generate_value('AreaLivingRooms')
        elif room_type == RoomType.BEDROOM:
            room.area = self.constraints.generate_value('AreaBedRooms')

            # If constraints told us we get an extra room, lets add it
            # Closet is an example of an extra room
            if self.constraints.generate_value('ExtraRoom') > 0:
                print('An Extra room(s) was generated in a bedroom')
                room.extra_rooms.insert(0, self.generate_valid_room(RoomType.EXTRA_ROOM))
        elif room_type == RoomType.KITCHEN:
            room.area = self.constraints.generate_value('AreaKitchens')
        elif room_type == room_type.BATHROOM:
            room.area = self.constraints.generate_value('AreaBathrooms')
        elif room_type == room_type.EXTRA_ROOM:
            room.area = self.constraints.generate_value('AreaCloset')

        return room

