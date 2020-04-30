from Constraints.ConstraintSet2 import ConstraintSet
from Constraints.MinMax import MinMax
from FloorPlan.Room import RoomType, Room
from FloorPlan.RoomNode import RoomNode


class SuburbanGenerator:

    def __init__(self):
        self.constraints = ConstraintSet()
        self.constraints.add('LivingRooms', MinMax(1, 1))
        self.constraints.add('AreaLivingRooms', MinMax(400, 500))

        self.constraints.add('BedRooms', MinMax(1, 2))
        self.constraints.add('AreaBedRooms', MinMax(400, 500))

        self.constraints.add('Bathrooms', MinMax(0, 1))
        self.constraints.add('AreaBathrooms', MinMax(200, 200))

        self.constraints.add('Kitchens', MinMax(0, 1))
        self.constraints.add('AreaKitchens', MinMax(200, 200))

        self.constraints.add('ExtraRoom', MinMax(0, 1))
        self.constraints.add('AreaCloset', MinMax(100, 100))

    def generate_floor_plan(self):
        main = self.generate_valid_room(RoomType.LIVING_ROOM)

        bedrooms = self.constraints.generate_value('BedRooms')
        bathrooms = self.constraints.generate_value('Bathrooms')
        kitchens = self.constraints.generate_value('Kitchens')

        print('Total bedrooms: ', bedrooms)
        print('Total bathrooms: ', bathrooms)
        print('Total kitchens: ', kitchens)

        # Generate bedrooms
        for i in range(bedrooms):
            main.children.insert(0, self.generate_valid_room(RoomType.BEDROOM))

        # Generate Bathrooms
        for i in range(bathrooms):
            main.children.insert(0, self.generate_valid_room(RoomType.BATHROOM))

        # Generate Kitchen
        for i in range(kitchens):
            main.children.insert(0, self.generate_valid_room(RoomType.KITCHEN))

        return main.to_floor_plan()

    def generate_valid_room(self, room_type:RoomType):
        room = RoomNode(room_type)

        if room_type == RoomType.LIVING_ROOM:
            room.area = self.constraints.generate_value('AreaLivingRooms')
        elif room_type == RoomType.BEDROOM:
            room.area = self.constraints.generate_value('AreaBedRooms')

            # If constraints told us we get an extra room, lets add it
            # Closet is an extample of an extra room
            if self.constraints.generate_value('ExtraRoom') > 0:
                print('An Extra room was generated in a bedroom')
                room.children.insert(0, self.generate_valid_room(RoomType.EXTRA_ROOM))
        elif room_type == RoomType.KITCHEN:
            room.area = self.constraints.generate_value('AreaKitchens')
        elif room_type == room_type.BATHROOM:
            room.area = self.constraints.generate_value('AreaBathrooms')
        elif room_type == room_type.EXTRA_ROOM:
            room.area = self.constraints.generate_value('AreaCloset')

        return room

