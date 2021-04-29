import glob
import os
import cv2
import argparse
from typing import Tuple, List
import WasuLib.settings as settings
from WasuLib.trace import Trace
from WasuLib.stage_prepare import prepare_data
from WasuLib.stage_divide import divide_data
from WasuLib.xml_image import XMLImage


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
        for i in range(len(list_image)):
            # Save sub data
            sub_image = list_image[i]
            sub_xml_obj = list_xml_obj[i]

            img_file_name = create_sub_name(img_path, i, save_directory)
            sub_xml_obj.image_filename = img_file_name.split(settings.SLASH)[-1]

            cv2.imwrite(img_file_name, sub_image)
            sub_xml_obj.save(create_sub_name(xml_path, i, save_directory))
            pass  # for i
        pass  # for xml_path
    pass  # main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Workflow environment fo dividing images and xml files")
    parser.add_argument('-d', '--read_directory', type=str, required=True,
                        help='Directory containing the images and xml files')
    parser.add_argument('-s', '--save_directory', type=str, required=True,
                        help='Save directory')
    parser.add_argument('--sub_size', type=int, nargs=2, required=True, metavar=('width', 'height'),
                        help='Sub image size')
    parser.add_argument('--prepare_multiply', type=int, nargs=2, required=True,
                        metavar=('width_scale', 'height_scale'), help='Prepared image size')
    args = parser.parse_args()
    stage_prepare_size = (args.sub_size[0] * args.prepare_multiply[0], args.sub_size[1] * args.prepare_multiply[1])
    main(args.read_directory, args.save_directory, args.sub_size, stage_prepare_size)
    pass

# main(
#     read_directory='images',
#     save_directory='images/out',
#     sub_size=(1024, 1024),
#     prepare_size=(4096, 4096)
# )
