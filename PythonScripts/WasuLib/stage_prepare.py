"""
Preparing image (and xml file) to detection (training process)
"""
import cv2
import numpy as np
from typing import Tuple
import WasuLib.settings as settings
from WasuLib.xml_image import XMLImage
from WasuLib.trace import Trace


def resize(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage) -> Tuple[settings.CV2_IMAGE, XMLImage]:
    return cv2.resize(image, shape2d[:2]), xml_obj.resize(shape2d)


def black_bars(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage) -> Tuple[settings.CV2_IMAGE, XMLImage]:
    h_img, w_img = image.shape
    h_out, w_out = shape2d
    if h_img > h_out or w_img > w_out:
        Trace(f"Given image ({image.shape}) is bigger than give output ({shape2d})",
              Trace.TRACE_WARNING, __file__, black_bars.__name__)
        image = image[:h_img, :w_img]
        pass
    new_image = np.zeros(shape2d).astype('uint8')
    new_image[:h_img, :w_img] = image
    return new_image, xml_obj.black_bars(shape2d)


def _cut_middle(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage) -> Tuple[settings.CV2_IMAGE, XMLImage]:
    raise NotImplementedError


def _cut_top_left(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage) -> Tuple[settings.CV2_IMAGE, XMLImage]:
    raise NotImplementedError


def _cut_top_right(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage) -> Tuple[settings.CV2_IMAGE, XMLImage]:
    raise NotImplementedError


def _cut_bottom_left(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage) -> Tuple[settings.CV2_IMAGE, XMLImage]:
    raise NotImplementedError


def _cut_bottom_right(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage) -> Tuple[settings.CV2_IMAGE, XMLImage]:
    raise NotImplementedError


def prepare_data(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage = None):
    if settings.STG_PREPARE_METHOD == settings.STAGE_PREPARE_IMAGE_RESIZE:
        image, xml_obj = resize(image, shape2d, xml_obj)
    elif settings.STG_PREPARE_METHOD == settings.STAGE_PREPARE_IMAGE_BLACK_BARS:
        image, xml_obj = black_bars(image, shape2d, xml_obj)
    elif settings.STG_PREPARE_METHOD == settings.STAGE_PREPARE_IMAGE_CUT_MIDDLE:
        image, xml_obj = _cut_middle(image, shape2d, xml_obj)
    elif settings.STG_PREPARE_METHOD == settings.STAGE_PREPARE_IMAGE_CUT_TOP_LEFT:
        image, xml_obj = _cut_top_left(image, shape2d, xml_obj)
    elif settings.STG_PREPARE_METHOD == settings.STAGE_PREPARE_IMAGE_CUT_TOP_RIGHT:
        image, xml_obj = _cut_top_right(image, shape2d, xml_obj)
    elif settings.STG_PREPARE_METHOD == settings.STAGE_PREPARE_IMAGE_CUT_BOTTOM_LEFT:
        image, xml_obj = _cut_bottom_left(image, shape2d, xml_obj)
    elif settings.STG_PREPARE_METHOD == settings.STAGE_PREPARE_IMAGE_CUT_BOTTOM_RIGHT:
        image, xml_obj = _cut_bottom_right(image, shape2d, xml_obj)
    else:
        Trace(f"Wrong STG_PREPARE_METHOD = {settings.STG_PREPARE_METHOD}",
              Trace.TRACE_ERROR, __file__, prepare_data.__name__)
    return image, xml_obj
