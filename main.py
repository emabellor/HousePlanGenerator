from FloorPlan.SuburbanGenerator import SuburbanGenerator
from FloorPlan.FloorPlan import FloorPlan
from FloorPlan.Room import RoomType
import cv2
import numpy as np


def main():
    generator = SuburbanGenerator()
    fp = generator.generate_floor_plan()

    show_floor_plan(fp)
    print('Done!')


def show_floor_plan(fp: FloorPlan):
    width = 252
    height = 252

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

    cv2.namedWindow('floor_plan', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('floor_plan', image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

