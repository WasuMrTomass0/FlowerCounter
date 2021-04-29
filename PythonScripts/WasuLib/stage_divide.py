from typing import List, Tuple

import cv2

import WasuLib.settings as settings
from WasuLib.xml_package.xml_image import XMLImage
from WasuLib.trace import Trace


def divide_data(image: settings.CV2_IMAGE, shape2d, xml_obj: XMLImage = None) \
        -> Tuple[List[settings.CV2_IMAGE], List[XMLImage]]:
    # -> List[Tuple[settings.CV2_IMAGE, XMLImage]]:
    """
    Divides image into smaller sub-images. Creates separate XMLImage objects
    :param image: prepared image
    :param shape2d: sub-image shape
    :param xml_obj: prepared xml object
    :return: List of pairs (tuples) image, xml object
    """
    h_img, w_img = image.shape[:2]
    h_sub, w_sub = shape2d

    sub_images = list()
    sub_xmls = list()
    # ret = list()
    # Images
    for h_start in range(0, h_img, h_sub):
        for w_start in range(0, w_img, w_sub):
            h_end = h_start + h_sub
            w_end = w_start + w_sub
            sub_images.append(image[h_start: h_end, w_start: w_end])
            pass  # for w_index
        pass  # for h_index

    # XMLImages
    sub_xmls = xml_obj.divide(shape2d)

    # Check correctness
    if len(sub_images) != len(sub_xmls):
        Trace(f"sub_images ({len(sub_images)}) differs from sub_xmls ({len(sub_xmls)})",
              Trace.TRACE_ERROR, __file__, divide_data.__name__)

    # # Prepare output
    # for i in range(min(len(sub_images), len(sub_xmls))):
    #     ret.append((sub_images[i], sub_xmls[i]))

    return sub_images, sub_xmls
