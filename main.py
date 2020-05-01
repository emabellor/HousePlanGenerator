from FloorPlan.SuburbanGenerator import SuburbanGenerator
from FloorPlan.FloorPlan import FloorPlan
from FloorPlan.Room import RoomType
from typing import List
import cv2
import numpy as np


def main():
    floor_generator_list: List[SuburbanGenerator] = []

    first_floor = SuburbanGenerator(300, 300)
    first_floor.set_static_room_number(RoomType.LIVING_ROOM, 1)
    first_floor.set_static_room_number(RoomType.KITCHEN, 1)
    first_floor.set_static_room_number(RoomType.BEDROOM, 1)
    first_floor.set_static_room_number(RoomType.BATHROOM, 1)
    first_floor.set_static_room_number(RoomType.EXTRA_ROOM, 1)
    floor_generator_list.append(first_floor)

    second_floor = SuburbanGenerator(250, 250)
    second_floor.set_static_room_number(RoomType.LIVING_ROOM, 0)
    second_floor.set_static_room_number(RoomType.KITCHEN, 0)
    second_floor.set_static_room_number(RoomType.BEDROOM, 2)
    second_floor.set_static_room_number(RoomType.BATHROOM, 1)
    second_floor.set_static_room_number(RoomType.EXTRA_ROOM, 1)
    floor_generator_list.append(second_floor)

    third_floor = SuburbanGenerator(250, 200)
    third_floor.set_static_room_number(RoomType.LIVING_ROOM, 0)
    third_floor.set_static_room_number(RoomType.KITCHEN, 0)
    third_floor.set_static_room_number(RoomType.BEDROOM, 1)
    third_floor.set_static_room_number(RoomType.BATHROOM, 0)
    third_floor.set_static_room_number(RoomType.EXTRA_ROOM, 0)
    floor_generator_list.append(third_floor)

    fp_list = generate_house_plan(floor_generator_list)
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
    for count, fp in enumerate(fp_list):
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

        name_window = 'Floor ' + str(count + 1)
        cv2.namedWindow(name_window, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(name_window, image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

