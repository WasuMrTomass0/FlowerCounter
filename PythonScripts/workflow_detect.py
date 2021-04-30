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


def workflow(image: settings.CV2_IMAGE, sub_size, prepare_size, xml_obj: XMLImage = None) -> \
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


def perform_detection(read_directory: str, extensions: List[str], min_score: float, sub_size, prepare_multiplier):
    img_paths = []
    for ext in extensions:
        img_paths += glob.glob(f"{read_directory}/*.{ext}")
        pass
    print(f"Got {len(img_paths)} images from {read_directory}")

    for img_path in img_paths:
        # Read image
        image = cv2.imread(img_path)
        # Run workflow
        prepare_size = (sub_size[0] * prepare_multiplier[0], sub_size[1] * prepare_multiplier[1])
        list_image = workflow(image, sub_size, prepare_size, None)[0]
        list_boxes = []
        # DETECTOR
        sub_image_index = -1
        for image in list_image:
            sub_image_index += 1
            # Detect
            detection_boxes, detection_classes, detection_scores = detector_function.detect_from_image(
                detector_function.detection_model, image)
            # Read boxes
            boxes = []
            for i in range(min(len(detection_boxes), len(detection_classes), len(detection_scores))):
                if detection_scores[i] < min_score:
                    continue
                w_sub_image_index = sub_image_index % prepare_multiplier[1]
                h_sub_image_index = sub_image_index // prepare_multiplier[1]
                x_min = int((detection_boxes[i][0] + w_sub_image_index) * sub_size[0])
                x_max = int((detection_boxes[i][2] + w_sub_image_index) * sub_size[0])
                y_min = int((detection_boxes[i][1] + h_sub_image_index) * sub_size[1])
                y_max = int((detection_boxes[i][3] + h_sub_image_index) * sub_size[1])
                label_index = detection_classes[i]
                label = detection_boxes.category_index[label_index]['name']
                score = detection_scores[i]
                # Store boxes for sub image
                boxes.append(BBox(x_min, y_min, x_max, y_max, label))
                pass  # for i
            # Add all boxes to this sub image
            list_boxes.append(boxes)
            pass  # for image

        # TODO Na ten moment bboxy maja juz globalne wspolrzedne (dla zdjecie prepare_stage)
        # po sprawdzeniu czy wszystko działa, wywalić boxes i zostawić jedną listę list_boxes

        pass  # for img_path


        pass
    pass  # main


MIN_SCORE_THRESHOLD = 0.2
SUB_IMAGE_WIDTH = 1024
SUB_IMAGE_HEIGHT = 1024

_DETECT_IMG_DIR = ''
_IMG_EXTENSIONS = ['']
_sub_size = (SUB_IMAGE_WIDTH, SUB_IMAGE_HEIGHT)
_prepare_multiplier = (4, 4)

perform_detection(_DETECT_IMG_DIR, _IMG_EXTENSIONS, MIN_SCORE_THRESHOLD, _sub_size, _prepare_multiplier)

if __name__ == '__main__':

    pass
