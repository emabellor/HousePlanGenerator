from FloorPlan.Room import RoomType
from Constraints.Constraint import Constraint
from DataStructures.SquarifiedTeeMap import SquarifiedTreeMap, Element
from typing import List
from FloorPlan.FloorPlan import FloorPlan
import random


class RoomNode:
    def __init__(self, room_type: RoomType):
        self.room_type = room_type
        self.children: List['RoomNode'] = []
        self.area = 0

    def to_floor_plan(self):
        # Default home size is 250 x 250
        return self.to_floor_plan_width_height(250, 250)

    def to_floor_plan_width_height(self, width, height):
        # min_slice_ratio = Constraint.get_random_number(25, 45) / 100
        # TODO revert this
        min_slice_ratio = 0

        # Generate our squarified tree map
        nodes = self.select_nodes()

        # We want to include our own area inside our tree map
        nodes.insert(0, Element(self, self.area))

        slice_item = SquarifiedTreeMap.get_slice(nodes, 1, min_slice_ratio)
        rectangles = SquarifiedTreeMap.get_rectangles_slice_item(slice_item, width, height)

        fp = FloorPlan()

        # Build our floorplan off our our tree map
        for r in rectangles:
            fp.add_room(r.x, r.y, r.width, r.height, r.slice_item.elements[0].obj.room_type)

            # Build our rooms internal tree map
            for child in r.slice_item.elements:
                # We ignore ourself and nodes without children
                if child.obj != self and len(child.obj.children) > 0:
                    # Child tree ma uses local coordinates of parent room
                    # We must offset these and then merge our floorplans
                    internal_fp = child.obj.to_floor_plan_width_height(r.width, r.height)
                    fp.merge_floor_plan_offset(internal_fp, r.x, r.y)

        # return our produced floor plan
        return fp

    """
    var nodes = Children
        .Select(x => new SquarifiedTreeMap.Element<RoomNode> { Object = x, Value = x.Area })
        .OrderBy(x => Constraint.GetRandomNumber(-100, 100))
        .ToList();
    """
    def select_nodes(self):
        list_items:List[Element] = []

        for item in self.children:
            list_items.append(Element(item, item.area))

        # Shuffle list
        random.shuffle(list_items)
        return list_items