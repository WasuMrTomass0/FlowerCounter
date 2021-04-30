import glob
import os
import cv2
# import argparse
from typing import Tuple, List
import WasuLib.settings as settings
from WasuLib.trace import Trace
from WasuLib.stage_prepare import prepare_data
from WasuLib.stage_divide import divide_data
from WasuLib.xml_image import XMLImage
import detector_function
from WasuLib.bounding_box import BBox


def workflow(image: settings.CV2_IMAGE, sub_size, prepare_size, xml_obj: XMLImage) -> \
        Tuple[List[settings.CV2_IMAGE], List[XMLImage]]:
    image, xml_obj = prepare_data(image, prepare_size, xml_obj)
    list_image, list_xml_obj = divide_data(image, sub_size, xml_obj)
    return list_image, list_xml_obj


def create_sub_name(base_name: str, cnt: int, directory: str = None):
    if directory is None:
        name = base_name.split('.')[0]
        ext = base_name.split('.')[-1]
        return f"{name}_{cnt}.{ext}"
    name = base_name.split(settings.SLASH)[-1].split('.')[0]
    ext = base_name.split('.')[-1]
    return os.path.join(directory, f"{name}_{cnt}.{ext}")


def main(read_directory: str, save_directory: str, sub_size, prepare_size):
    xml_paths = glob.glob(f"{read_directory}/*.xml")
    Trace(f"read_directory is '{read_directory}' got {len(xml_paths)} to '{save_directory}'\nsub_size is {sub_size}"
          f"\tprepare_size is {prepare_size}", Trace.TRACE_INFO, __file__, main.__name__)

    for xml_path in xml_paths:
        # Create xml object
        xml_obj = XMLImage(xml_path=xml_path)
        # Read image path
        img_path = xml_obj.image_path()
        # Read image
        image = cv2.imread(img_path)
        # Run workflow
        list_image, list_xml_obj = workflow(image, sub_size, prepare_size, xml_obj)
        # DETECTOR
        for image in list_image:
            detection_boxes, detection_classes, detection_scores = detector_function.detect_from_image(
                detector_function.detection_model, image)

            for i in range(min(len(detection_boxes), len(detection_classes), len(detection_scores))):
                if detection_scores[i] < MIN_SCORE_THRESHOLD:
                    continue

                x_min = int(detection_boxes[i][0] * SUB_IMAGE_WIDTH)
                print(f"x_min {x_min}")
                x_max = int(detection_boxes[i][2] * SUB_IMAGE_WIDTH)
                print(f"x_max {x_max}")
                y_min = int(detection_boxes[i][1] * SUB_IMAGE_HEIGHT)
                print(f"y_min {y_min}")
                y_max = int(detection_boxes[i][3] * SUB_IMAGE_HEIGHT)
                print(f"y_max {y_max}")

                label_index = detection_classes[i]
                print(f"label_index {label_index}")
                label = detection_boxes.category_index[label_index]
                print(f"label {label}")
                score = detection_scores[i]
                print(f"score {score}")

                pass  # for i
            pass  # for image
        pass  # for xml_path
    pass  # main


MIN_SCORE_THRESHOLD = 0.2
SUB_IMAGE_WIDTH = 1024
SUB_IMAGE_HEIGHT = 1024
