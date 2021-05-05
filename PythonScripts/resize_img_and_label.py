import cv2
import glob
import argparse
from typing import Tuple
from WasuLib.xml_image import XMLImage
from WasuLib.stage_prepare import resize


def main(directory: str, shape2d: Tuple[int, int]):
    # Counters 
    print(type(shape2d), shape2d)
    cnt = 0
    cnt_no_resize_needed = 0
    paths = glob.glob(f"{directory}/*.xml")
    print(f"Found {len(paths)} xml files in {directory}")

    for xml_path in paths:
        cnt += 1
        xml_obj = XMLImage(xml_path=xml_path)
        image_path = xml_obj.image_path()
        image = cv2.imread(image_path)
        if xml_obj.height == shape2d[1] and xml_obj.width == shape2d[0]:
            cnt_no_resize_needed += 1
            continue
        image, xml_obj = resize(image, shape2d, xml_obj)

        cv2.imwrite(image_path, image)
        xml_obj.save()
        pass
    # Show summarry
    print(f"Processed {cnt} images. {cnt_no_resize_needed} image were already in good size. Output size was {shape2d}.")
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rescale images and xml labels")

    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')

    parser.add_argument('-s', '--size', type=int, nargs=2, required=True, metavar=('width', 'height'),
                        help='Image size')
    
    args = parser.parse_args()
    main(args.directory, args.size)
    pass
