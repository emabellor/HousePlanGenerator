from FloorPlan.SuburbanGenerator import SuburbanGenerator
from FloorPlan.FloorPlan import FloorPlan
from FloorPlan.Room import RoomType
from typing import List
import cv2
import numpy as np
import json


def main():
    floor_generator_list: List[SuburbanGenerator] = []

    first_floor = SuburbanGenerator(width=300, height=300, length=9, name='First Floor')
    first_floor.set_static_room_number(RoomType.LIVING_ROOM, 1)
    first_floor.set_static_room_number(RoomType.KITCHEN, 1)
    first_floor.set_static_room_number(RoomType.BEDROOM, 1)
    first_floor.set_static_room_number(RoomType.BATHROOM, 1)
    first_floor.set_static_room_number(RoomType.EXTRA_ROOM, 1)
    first_floor.set_static_room_number(RoomType.STAIRCASE, 1)
    floor_generator_list.append(first_floor)

    second_floor = SuburbanGenerator(width=250, height=250, length=9, name='Second Floor')
    second_floor.set_static_room_number(RoomType.LIVING_ROOM, 0)
    second_floor.set_static_room_number(RoomType.KITCHEN, 0)
    second_floor.set_static_room_number(RoomType.BEDROOM, 2)
    second_floor.set_static_room_number(RoomType.BATHROOM, 1)
    second_floor.set_static_room_number(RoomType.EXTRA_ROOM, 1)
    floor_generator_list.append(second_floor)

    third_floor = SuburbanGenerator(width=250, height=200, length=9, name='Third Floor')
    third_floor.set_static_room_number(RoomType.LIVING_ROOM, 0)
    third_floor.set_static_room_number(RoomType.KITCHEN, 0)
    third_floor.set_static_room_number(RoomType.BEDROOM, 1)
    third_floor.set_static_room_number(RoomType.BATHROOM, 0)
    third_floor.set_static_room_number(RoomType.EXTRA_ROOM, 0)
    floor_generator_list.append(third_floor)

    fp_list = generate_house_plan(floor_generator_list)
    json_obj = generate_json_obj(fp_list)

    with open('jsonHousePlan.json', 'w') as file:
        file.write(json.dumps(json_obj, indent=True))

    show_house_plan(fp_list)
    print('Done!')


def generate_house_plan(floor_generator_list: List[SuburbanGenerator]):
    # Check dimensions integrity
    if len(floor_generator_list) == 0:
        raise Exception('There are no floors to be generated')

    for i in range(len(floor_generator_list) - 1 ):
        lower_floor = floor_generator_list[i]
        upper_floor = floor_generator_list[i + 1]

        if upper_floor.width > lower_floor.width:
            raise Exception('The width of the upper floor cannot be higher than the lower floor')

        if upper_floor.height > lower_floor.height:
            raise Exception('The height of the upper floor cannot be higher than the lower floor')

    fp_list: List[FloorPlan] = []

    # Generate floor plans
    for i in range(len(floor_generator_list)):
        fp = floor_generator_list[i].generate_floor_plan()
        fp_list.append(fp)

    return fp_list


def show_house_plan(fp_list: List[FloorPlan]):
    for fp in fp_list:
        width = fp.width + 1
        height = fp.height + 1

        image = np.zeros((height, width, 3), np.uint8)
        image[:] = 255

        colors = [
            (128, 128, 128),  # gray
            (169, 169, 169),  # dark gray
            (211, 211, 211),  # light gray
            (119, 136, 153),  # light slate gray
            (192, 192, 192)   # silver
        ]

        # Draw rooms and their types
        for i in range(len(fp.rooms)):
            r = fp.rooms[i]
            start_point = (r.x, r.y)
            end_point = (r.x + r.width, r.y + r.height)
            color = colors[i % len(colors)]

            cv2.rectangle(image, start_point, end_point, color, -1)
            cv2.rectangle(image, start_point, end_point, (0, 0, 0), 1)

            text_to_put = r.room_type.name
            font_scale = 0.3
            thickness = 1
            text_width, text_height = cv2.getTextSize(text_to_put, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            cv2.putText(image, text_to_put, (r.x + 5, r.y + text_height + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness)

        name_window = fp.name
        cv2.namedWindow(name_window, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(name_window, image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


def generate_json_obj(fp_list: List[FloorPlan]):
    print('Generating JSON File')

    json_obj = {
        'name': 'My House Plan',
        'type': 'flat',
        'width': fp_list[0].width,
        'height': fp_list[0].height,
        'floors': []
    }

    for floor_idx, fp in enumerate(fp_list):
        json_floor = {
            'name': fp.name,
            'width': fp.width,
            'height': fp.height,
            'noOfRooms': len(fp.rooms),
            'roof': 'roof' if floor_idx == len(fp_list) - 1 else 'ceiling',
            'rooms': []
        }

        for room_idx, room in enumerate(fp.rooms):
            # Walls, windows and doors logic
            # North obj
            json_north = {
                'direction': 'north',
                'type': 'external' if room.y == 0 else 'internal',
                'length': room.width,
                'doors': []
            }
            check_window(room, json_north)
            for room_adj in fp.rooms:
                if room_adj == room:
                    continue
                if room.y == room_adj.y + room_adj.height:
                    check_adjacency_x(room, room_adj, json_north)

            # East obj
            json_east = {
                'direction': 'east',
                'type': 'external' if room.x == 0 else 'internal',
                'length': room.height,
                'doors': []
            }
            check_window(room, json_east)
            for room_adj in fp.rooms:
                if room_adj == room:
                    continue
                if room.x == room_adj.x + room_adj.width:
                    check_adjacency_y(room, room_adj, json_east)

            # West obj
            json_west = {
                'direction': 'west',
                'type': 'external' if room.x + room.width == fp.width else 'internal',
                'length': room.height,
                'doors': []
            }
            check_window(room, json_west)
            for room_adj in fp.rooms:
                if room_adj == room:
                    continue
                if room.x + room.width ==  room_adj.x:
                    check_adjacency_y(room, room_adj, json_west)

            # South obj
            json_south = {
                'direction': 'south',
                'type': 'external' if room.y + room.height == fp.height else 'internal',
                'length': room.width,
                'doors': []
            }
            check_window(room, json_south)
            for room_adj in fp.rooms:
                if room_adj == room:
                    continue
                if room.y + room.height == room_adj.y:
                    check_adjacency_x(room, room_adj, json_south)

            json_walls = [
                json_north,
                json_east,
                json_west,
                json_south
            ]

            # Put the external door in the living room
            if room.room_type == RoomType.LIVING_ROOM:
                for wall in json_walls:
                    if wall['type'] == 'external':
                        wall['doors'].append({
                            'location': 0,
                            'type': 'external',
                            'to': 'STREET'
                        })
                        break

            json_room = {
                'name': room.room_type.name,
                'x': room.x,
                'y': room.y,
                'walls': json_walls,
            }

            json_floor['rooms'].append(json_room)

        json_obj['floors'].append(json_floor)

    print('Done generating JSON')
    return json_obj


def check_window(room, json_wall_obj):
    if (json_wall_obj['type'] == 'external'
            and room.room_type != RoomType.EXTRA_ROOM and room.room_type != RoomType.BATHROOM):
        json_wall_obj['window'] = True
    else:
        json_wall_obj['window'] = False


def check_adjacency_x(room, room_adj, json_wall_obj):
    if room_adj.x <= room.x < room_adj.x + room_adj.width:
        json_wall_obj['doors'].append({
            'location': 0,
            'type': 'internal',
            'to': room_adj.room_type.name
        })
    elif room.x <= room_adj.x < room.x + room.width:
        json_wall_obj['doors'].append({
            'location': room_adj.x - room.x,
            'type': 'internal',
            'to': room_adj.room_type.name
        })


def check_adjacency_y(room, room_adj, json_wall_obj):
    if room_adj.y <= room.y < room_adj.y + room_adj.height:
        json_wall_obj['doors'].append({
            'location': 0,
            'type': 'internal',
            'to': room_adj.room_type.name
        })
    elif room.y <= room_adj.y < room.y + room.height:
        json_wall_obj['doors'].append({
            'location': room_adj.y - room.y,
            'type': 'internal',
            'to': room_adj.room_type.name
        })


if __name__ == '__main__':
    main()

