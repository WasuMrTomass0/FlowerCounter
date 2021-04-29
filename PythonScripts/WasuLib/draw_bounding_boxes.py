import cv2
from copy import deepcopy
from typing import List
import time
from WasuLib.settings import CV2_IMAGE
from WasuLib.bounding_box import BBox
import WasuLib.settings as settings
from WasuLib.trace import Trace
if settings.RUNNING_IN_COLAB:
    from google.colab.patches import cv2_imshow

_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255)
]


def _color_by_label(label: str, labels: List[str]):
    if not labels:
        return _colors[0]
    arg = labels.index(label)
    if arg == -1 or arg >= len(_colors):
        arg = len(_colors) - 1
    return _colors[arg]


def _show_image_colab(window_name: str, image: settings.CV2_IMAGE, delay: int):
    Trace(f"Image's window name: {window_name}", Trace.TRACE_DEBUG, __file__, _show_image_colab.__name__)
    cv2_imshow(image)
    delay = min(1, delay)
    time.sleep(delay / 1000)
    pass


def _show_image_cv2(window_name: str, image: settings.CV2_IMAGE, delay: int):
    cv2.imshow(window_name, image)
    cv2.waitKey(delay)
    pass


_show_image = _show_image_colab if settings.RUNNING_IN_COLAB else _show_image_cv2


def draw_bounding_boxes(image: CV2_IMAGE, boxes: List[BBox], win_name: str = 'bounding_boxes',
                        labels: List[str] = None, thickness: int = 2, delay: int = 0,
                        dot_center: bool = True):
    copied_image = deepcopy(image)
    show_label = type(labels) == list
    for box in boxes:
        color = _color_by_label(box.label, labels)
        if dot_center:
            cv2.circle(copied_image, (box.x_centre, box.y_centre), 2, (0, 0, 255), 3)
        cv2.rectangle(copied_image, (box.x_min, box.y_min), (box.x_max, box.y_max), color, thickness)
        if show_label:
            cv2.putText(copied_image, box.label, (box.x_min, box.y_min), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        pass  # for box
    _show_image(win_name, copied_image, delay)
    return copied_image
