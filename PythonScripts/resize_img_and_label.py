from PIL import Image
import os
import glob
import argparse
import xmltodict
# import dicttoxml
from dict2xml import dict2xml


def rescale_coordinate(str_coordinate, scale):
    return int(int(str_coordinate) * scale)


def read_label_file_xml(xml_file_path):
    with open(xml_file_path, 'r') as token:
        xml = token.read()
    xml = xmltodict.parse(xml)
    # Read img name
    img_name = xml['annotation']['filename']
    img_path = xml_file_path.split('.')[0] + '.' + img_name.split('.')[-1]
    # Read BBoxes info
    objects = xml['annotation']['object']
    # Single bboxes in image are stored differently than multiple bbonxes
    if type(objects) != list:
        objects = [objects]
    bboxes = []
    classes = []
    for obj in objects:
        classes.append(obj['name'])
        bboxes.append((
            int(obj['bndbox']['xmin']), 
            int(obj['bndbox']['ymin']), 
            int(obj['bndbox']['xmax']), 
            int(obj['bndbox']['ymax'])
        ))
        pass
    
    return img_name, img_path, bboxes, classes


def main(directory, new_size):
    # Counters 
    cnt = 0
    cnt_no_resize_needed = 0
    # New size
    w_new, h_new = new_size
    # Read all xml files in directory
    paths = glob.glob(f"{directory}/*.xml")
    # Show info
    print(f"Found {len(paths)} xml files in {directory}")
    # Iterate xml_files
    for xml_file in paths:
        # Show progress info
        cnt += 1
        print(cnt, end="\r")
        # Read file
        with open(xml_file, 'r') as token:
            xml = token.read()
        # Convert to dict
        xml = xmltodict.parse(xml)
        # Read image name
        img_name = xml['annotation']['filename']
        # Create image path
        img_path = os.path.join(directory, img_name)
        # Read image
        im_original = Image.open(os.path.join(directory, img_path))
        # Read original image size
        w_old, h_old = im_original.size[:2]
        # If resize is not needed continue
        if w_new == w_old and h_new == h_old:
            cnt_no_resize_needed += 1
            continue
        # Resize and save image 
        im_resized = im_original.resize(new_size, Image.ANTIALIAS)
        im_resized.save(os.path.join(directory, img_path))
        # Calculate resize scale 
        x_scale = w_new / w_old
        y_scale = h_new / h_old
        # Change image size in xml
        xml['annotation']['size']['width'] = w_new
        xml['annotation']['size']['height'] = h_new
        # Read bounding boxes data from xml dict
        objects = xml['annotation']['object']
        # Single bboxes in image are stored differently than multiple bbonxes
        if type(objects) != list:
            objects = [objects]
        # Resize bounding boxes
        for obj in objects:
            obj['bndbox']['xmin'] = rescale_coordinate(obj['bndbox']['xmin'], x_scale)
            obj['bndbox']['xmax'] = rescale_coordinate(obj['bndbox']['xmax'], x_scale)
            obj['bndbox']['ymin'] = rescale_coordinate(obj['bndbox']['ymin'], y_scale)
            obj['bndbox']['ymax'] = rescale_coordinate(obj['bndbox']['ymax'], y_scale)
            pass
        # Save resized data into xml file
        xml = dict2xml(xml)
        with open(os.path.join(directory, xml_file), 'w') as token:
            token.write(xml)
        pass
    # Show summarry
    print(f"Processed {cnt} images. {cnt_no_resize_needed} image were already in good size. Output size was {new_size}.")
    pass

"""
def main(directory, size, img_ext="JPG"):
    # New size
    w_new, h_new = size
    cnt = 0
    # Iterate
    for img in os.listdir(directory):
        if not '.' + img_ext in img:
            continue
        # Resize image
        im = Image.open(os.path.join(directory, img))
        im_resized = im.resize(size, Image.ANTIALIAS)
        im_resized.save(os.path.join(directory, img))
        # Calculate scale
        w_old, h_old = im.size[:2]
        if w_new == w_old and h_new == h_old:
            cnt += 1
            print(f"{cnt} OK", end="\r")
            continue
        x_scale = w_new / w_old
        y_scale = h_new / h_old
        # Read xml file as dict
        xml_name = img.split('.')[0] + '.xml'
        with open(os.path.join(directory, xml_name), 'r') as token:
            xml = token.read()
        xml = xmltodict.parse(xml)
        # Change image size in xml
        xml['annotation']['size']['width'] = w_new
        xml['annotation']['size']['height'] = h_new
        # Change bounding boxes size in xml
        objects = xml['annotation']['object']
        # Single bboxes in image are stored differently than multiple bbonxes
        if type(objects) != list:
            objects = [objects]
        # Iterate
        for obj in objects:
            obj['bndbox']['xmin'] = rescale_coordinate(obj['bndbox']['xmin'], x_scale)
            obj['bndbox']['xmax'] = rescale_coordinate(obj['bndbox']['xmax'], x_scale)
            obj['bndbox']['ymin'] = rescale_coordinate(obj['bndbox']['ymin'], y_scale)
            obj['bndbox']['ymax'] = rescale_coordinate(obj['bndbox']['ymax'], y_scale)
            pass
        # Save xml
        # xml = dicttoxml.dicttoxml(xml, root=False, ids=False, attr_type=False).toprettyxml()
        xml = dict2xml(xml)
        with open(os.path.join(directory, xml_name), 'w') as token:
            token.write(xml)
            pass
        # Show progress
        cnt += 1
        print(cnt, end="\r")
        pass
    print(f"Processed {cnt} images. Output size was {size}.")
    pass
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rescale images and xml labels")

    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')

    parser.add_argument('-s', '--size', type=int, nargs=2, required=True, metavar=('width', 'height'),
                        help='Image size')
    
    args = parser.parse_args()
    main(args.directory, args.size)
    pass
