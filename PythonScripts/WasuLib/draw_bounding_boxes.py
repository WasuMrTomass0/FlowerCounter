import cv2
from copy import deepcopy
from typing import List
from WasuLib.settings import CV2_IMAGE
from WasuLib.bounding_box import BBox


colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255)
]


def color_by_label(label: str, labels: List[str]):
    if not labels:
        return colors[0]
    arg = labels.index(label)
    if arg == -1 or arg >= len(colors):
        arg = len(colors) - 1
    return colors[arg]


def draw_bounding_boxes(image: CV2_IMAGE, boxes: List[BBox], win_name: str = 'bounding_boxes',
                        labels: List[str] = None, thickness: int = 2, delay: int = 0,
                        dot_center: bool = True):
    copied_image = deepcopy(image)
    for box in boxes:
        color = color_by_label(box.label, labels)
        cv2.circle(copied_image, (box.x_centre, box.y_centre), 2, (0, 0, 255), 3)
        cv2.rectangle(copied_image, (box.x_min, box.y_min), (box.x_max, box.y_max), color, thickness)
        cv2.putText(copied_image, box.label, (box.x_min, box.y_min), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        pass  # for box
    cv2.imshow(win_name, copied_image)
    cv2.waitKey(delay)
    return copied_image
