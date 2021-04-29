import glob
import argparse
from WasuLib.xml_image import XMLImage


def check_img_sizes_from_xml(directory):
    # Read all xml files in directory
    paths = glob.glob(f"{directory}/*.xml")
    # Show info
    print(f"Found {len(paths)} xml files in {directory}")
    # Prepare dict
    shapes = dict()
    # Read all sizes from xml files:
    for xml_path in paths:
        xml_obj = XMLImage(xml_path=xml_path)
        img_size = (xml_obj.width, xml_obj.height, xml_obj.depth)
        # Store size
        if img_size in shapes:
            shapes[img_size] += 1
        else:
            shapes[img_size] = 1
        pass
    # Show counted sizes
    for key, value in shapes.items():
        print(f"\tShape: {' x '.join(key)}, \tNum: {value}")
        pass
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Count image sizes using xml")
    parser.add_argument('-d', '--directory', type=str, required=True,
                        help='Directory containing the images and xml files')
    args = parser.parse_args()
    check_img_sizes_from_xml(args.directory)
    pass
