from typing import List, Generic


class Element:
    def __init__(self, obj, value):
        self.obj = obj
        self.value = value


class Slice:
    def __init__(self, elements: List[Element], size, sub_slices: List['Slice']):
        self.elements = elements
        self.size = size
        self.sub_slices = sub_slices


class SliceResult:
    def __init__(self, elements, elements_size, remaining_elements):
        self.elements = elements
        self.elements_size = elements_size
        self.remaining_elements = remaining_elements


class SliceRectangle:
    def __init__(self, slice_item: Slice, x, y, width, height):
        self.slice_item = slice_item
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class SquarifiedTreeMap:

    @staticmethod
    def get_slice(elements: List[Element], total_size, slice_width):
        if len(elements) == 0:
            return None

        if len(elements) == 1:
            return Slice(elements, total_size, [])

        slice_result = SquarifiedTreeMap.get_elements_from_slice(elements, slice_width)

        sub_slices = [SquarifiedTreeMap.get_slice(slice_result.elements, slice_result.elements_size, slice_width),
                      SquarifiedTreeMap.get_slice(slice_result.remaining_elements, 1 - slice_result.elements_size,
                                                  slice_width)]

        return Slice(elements, total_size, sub_slices)

    @staticmethod
    def get_elements_from_slice(elements: List[Element], slice_width):
        elements_in_slice = []
        remaining_elements = []
        current = 0

        total = 0
        for element in elements:
            total += element.value

        for element in elements:
            if current > slice_width:
                remaining_elements.append(element)
            else:
                elements_in_slice.append(element)
                current += element.value / total

        return SliceResult(elements_in_slice, current, remaining_elements)

    @staticmethod
    def get_rectangles_slice_item(slice_item: Slice, width, height):
        area = SliceRectangle(slice_item, 0, 0, width, height)

        for rect in SquarifiedTreeMap.get_rectangles(area):
            # Make sure no rectangle go outside the original area
            if rect.x + rect.width > area.width:
                rect.width = area.width - rect.x
            if rect.y + rect.height > area.height:
                rect.height = area.height - rect.y

            yield rect

    @staticmethod
    def get_rectangles(slice_rectangle: SliceRectangle):
        is_horizontal_split = slice_rectangle.width >= slice_rectangle.height
        current_pos = 0
        for sub_slice in slice_rectangle.slice_item.sub_slices:
            sub_rect = SliceRectangle(sub_slice, 0, 0, 0, 0)
            rect_size = 0

            if is_horizontal_split:
                rect_size = round(slice_rectangle.width * sub_slice.size)
                sub_rect.x = slice_rectangle.x + current_pos
                sub_rect.y = slice_rectangle.y
                sub_rect.width = rect_size
                sub_rect.height = slice_rectangle.height
            else:
                rect_size = round(slice_rectangle.height * sub_slice.size)
                sub_rect.x = slice_rectangle.x
                sub_rect.y = slice_rectangle.y + current_pos
                sub_rect.width = slice_rectangle.width
                sub_rect.height = rect_size

            current_pos += rect_size
            if len(sub_slice.elements) > 1:
                for sr in SquarifiedTreeMap.get_rectangles(sub_rect):
                    yield sr
            elif len(sub_slice.elements) == 1:
                yield sub_rect