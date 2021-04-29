import argparse
import glob
import os
import cv2
from WasuLib.draw_bounding_boxes import draw_bounding_boxes
from WasuLib.xml_image import XMLImage


USE_COLAB_IMSHOW = False
DEF_DELAY = 1
DEF_MAX_COUNTER = -1
DEF_THICKNESS = 2
DEF_LABELS_FILE = None


def main(directory: str, delay: int, max_cnt: int, thickness: int,
         labels_path: str, show_box_centres: bool):
    xml_paths = glob.glob(os.path.join(directory, "*.xml"))  # Search for xml files
    max_cnt = max_cnt if max_cnt >= 0 else len(xml_paths)
    cnt = 0
    # Read labels from file
    show_labels = labels_path is not None
    if show_labels:
        with open(labels_path, 'r') as token:
            labels = token.read().split('\n')
        pass
    else:
        labels = None

    for xml_path in xml_paths:
        if cnt >= max_cnt:
            break

        xml_obj = XMLImage(xml_path=xml_path)
        img_path = xml_obj.image_path()
        image = cv2.imread(img_path)
        draw_bounding_boxes(image, xml_obj.boxes_classes, labels=labels, thickness=thickness, delay=delay,
                            dot_center=show_box_centres)
        cnt += 1
        pass  # for xml_path
    pass  # def main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Show labelled images in directory")

    parser.add_argument('-dir', '--directory', type=str, required=True,
                        help='Directory containing labelled images')

    parser.add_argument('-lab', '--labels', type=str, required=False, default=DEF_LABELS_FILE,
                        help='[Optional] Path to file with labels in each line. Default do not show labels')

    parser.add_argument('-delay', '--delay', type=int, required=False, default=DEF_DELAY,
                        help=f'[Optional] Delay between images [ms]. Pass 0 to skip manually. Default is {DEF_DELAY}')
    
    parser.add_argument('-max', '--max_counter', type=int, required=False, default=DEF_MAX_COUNTER,
                        help=f'[Optional] How many images to show. -1 to show all. Default is {DEF_MAX_COUNTER}')
    
    parser.add_argument('-t', '--thickness', type=int, required=False, default=DEF_THICKNESS,
                        help=F'[Optional] Rectangle thickness. Default is {DEF_THICKNESS}')

    parser.add_argument('-centre', action='store_true', help='Show centre of the box')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    args = parser.parse_args()
    main(
        directory=args.directory,
        delay=args.delay,
        max_cnt=args.max_counter,
        thickness=args.thickness,
        labels_path=args.labels,
        show_box_centres=args.centre
    )
    pass
