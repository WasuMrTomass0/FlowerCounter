import glob
import cv2
import xmltodict
from dict2xml import dict2xml
import argparse


def correct_labels_from_xml(dir, minimal_box_shape, old_class, new_class, skip_lower):
    # Read all xml files in directory
    paths = glob.glob(f"{dir}/*.xml")
    # Show info
    print(f"Found {len(paths)} xml files in {dir}")
    # Prepare dict
    classes = dict()
    incorrect_boxes = 0
    X_MIN_WIDTH, Y_MIN_HEIGHT = minimal_box_shape
    if not old_class or not new_class:
        CHANGE_CLASS = False
    else:
        # old_class = old_class.lower()
        # new_class = new_class.lower()
        CHANGE_CLASS = True
    # Read all sizes from xml files:
    for xml_file in paths:
        SAVE_XML_FILE = False
        # Read file
        with open(xml_file, 'r') as token:
            xml = token.read()
        # Convert to dict
        xml = xmltodict.parse(xml)
        # Read BBoxes info
        objects = xml['annotation']['object']
        # Single bboxes in image are stored differently than multiple bbonxes
        if type(objects) != list:
            objects = [objects]
        # Iterate through bound boxes
        for obj in objects:
            # Read data 
            c = obj['name']
            x_min = int(obj['bndbox']['xmin'])
            x_max = int(obj['bndbox']['xmax'])
            y_min = int(obj['bndbox']['ymin'])
            y_max = int(obj['bndbox']['ymax'])
            # Store class
            if c in classes:
                classes[c] += 1
            else:
                classes[c] = 1
            # Check box correctness
            if x_max - x_min > X_MIN_WIDTH or y_max - y_min > Y_MIN_HEIGHT:
                incorrect_boxes += 1
                pass 
            # Swap class name
            if CHANGE_CLASS and c == old_class:
                obj['name'] = new_class
                SAVE_XML_FILE = True
                pass
            # Make sure class name is lower
            elif not skip_lower and c.lower() != c:
                obj['name'] = c.lower()
                SAVE_XML_FILE = True
                pass
            pass  # for obj in objects

        # Save xml
        if SAVE_XML_FILE:
            # Save resized data into xml file
            xml = dict2xml(xml)
            with open(xml_file, 'w') as token:
                token.write(xml)
            pass
        pass  # for xml_file in paths
    # Show counted sizes
    print("Class".ljust(12, ' ') + "- \tNum")
    for key, value in classes.items():
        print(f"  {key.ljust(10, ' ')}- \t  {value}")
        pass
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rescale images")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    parser.add_argument('-old', '--old', type=str, required=False, default="", help='Replaced class name')
    parser.add_argument('-new', '--new', type=str, required=False, default="", help='Inserted class name')
    parser.add_argument('-s', '--shape', type=int, nargs=2, required=True, metavar=('width', 'height'),
                        help='Minimal bounding box dimensions')
    parser.add_argument('-skip_lower', action='store_true', help='Skip changing classes to lower string')
    
    args = parser.parse_args()
    
    directory = args.directory
    old = args.old
    new = args.new
    skip = args.skip_lower
    shape = args.shape
    
    print("Before:")
    # dir, minimal_box_shape, old_class, new_class, skip_lower
    correct_labels_from_xml(directory, shape, old, new, skip)
    print("\nAfter:")
    correct_labels_from_xml(directory, shape, None, None, True)
    pass
