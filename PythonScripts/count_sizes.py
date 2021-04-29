import glob
import argparse
from WasuLib.xml_image import XMLImage


def add_key_counter(key, dictionary) -> None:
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1
        pass
    pass


def check_img_sizes_from_xml(directory):
    # Read all xml files in directory
    paths = glob.glob(f"{directory}/*.xml")
    # Show info
    print(f"Found {len(paths)} xml files in {directory}")
    # Prepare dict
    img_shapes = dict()
    box_areas = dict()
    labels = dict()
    # Read all sizes from xml files:
    for xml_path in paths:
        xml_obj = XMLImage(xml_path=xml_path)
        img_size = (xml_obj.width, xml_obj.height, xml_obj.depth)
        # Store size
        add_key_counter(img_size, img_shapes)

        for box in xml_obj.boxes_classes:
            # Box label
            label = box.label
            add_key_counter(label, labels)
            # Box area
            b_area = box.area
            add_key_counter(b_area, box_areas)
        pass
    # Show counted sizes
    print(f'Image size:')
    for key, value in img_shapes.items():
        print(f"\t{'x'.join([str(elem) for elem in key]).ljust(10)} -> {value} time(s)")
        pass

    print(f'\nLabels:')
    # Show counted labels
    for key, value in labels.items():
        _key = ("'" + key + "'").ljust(10)
        print(f"\t{_key} -> {value} time(s)")
        pass

    # print(f'\nBounding boxes:')
    # for key, value in box_areas.items():
    #     print(f"\t{str(key).ljust(6)} -> {value} time(s)")
    #     pass
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Count image sizes using xml")
    parser.add_argument('-d', '--directory', type=str, required=True,
                        help='Directory containing the images and xml files')
    args = parser.parse_args()
    check_img_sizes_from_xml(args.directory)
    pass
