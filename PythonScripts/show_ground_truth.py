import cv2
import time
import argparse
import glob
import os
import xmltodict


USE_COLAB_IMSHOW = False
RECTANGLE_THICKNESS = 2

class_dict = dict()
def classes_to_int(class_name):
    if not class_name in class_dict:
        class_dict[class_name] = len(class_dict.keys()) + 1
    return class_dict[class_name] 


def classes_to_color(class_name):
    val = classes_to_int(class_name)
    if val == 1:
        return (255, 0, 0)
    elif val == 2:
        return (255, 255, 0)
    elif val == 3:
        return (255, 0, 255)
    elif val == 4:
        return (0, 255, 0)
    elif val == 5:
        return (0, 0, 255)
    elif val == 6:
        return (0, 255, 255)
    elif val == 7:
        return (125, 255, 0)
    elif val == 8:
        return (0, 125, 255)
    elif val == 8:
        return (0, 125, 255)
    else:
        return (125, 125, 125)
    pass


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


# bboxes = list of (xmin, ymin, xmax, ymax)
def read_img_show_bboxes(img_path, bboxes_list, classes):
    # Read image
    image = cv2.imread(img_path)
    # Add bboxes
    for i in range(len(bboxes_list)):
        # image.rectangle(bbox, fill=None, outline=None, width=1)
        bbox = bboxes_list[i]
        start_point = bbox[:2]
        end_point = bbox[2:]
        color = classes_to_color(classes[i])
        cv2.rectangle(image, start_point, end_point, color, RECTANGLE_THICKNESS)
        pass
    # Show image
    if USE_COLAB_IMSHOW:
        # cv2_imshow(image)
        filename = "BEKAMOCNO.png"
        cv2.imwrite(filename, image)
        display(Image(filename))
        # os.system(f"rm {filename}")
    else:
        cv2.imshow('image', image)
        cv2.waitKey(1)
    pass


def main(directory, delay, max_cnt):
    counter = 0
    # Read label files in directory
    paths = glob.glob(os.path.join(directory, "*.xml"))
    if max_cnt == -1:
        max_cnt = len(paths)
    for path in paths:
        counter += 1
        if counter > max_cnt:
            break
        try:
            # Read from xml
            img_name, img_path, bboxes, classes = read_label_file_xml(path)
            # Read and show image with bboxes
            read_img_show_bboxes(img_path, bboxes, classes)
            # Delay
            time.sleep(delay)
            
        except ValueError as err:
            print(f"Exception occured. File: f{path}.\nError {str(err)}")
        pass  # for path
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Show labelled images in directory")

    parser.add_argument('-dir', '--directory', type=str, required=True, help='Directory containing labelled images')

    parser.add_argument('-delay', '--delay', type=int, required=True, help='Delay between images')
    
    parser.add_argument('-max', '--max_counter', type=int, required=True, help='How many images to show. -1 to show all')
    
    parser.add_argument('-t', '--thickness', type=int, required=True, help='Rectangle thickness')
    
    parser.add_argument('-c', action='store_true', help='Use Colab imshow version')
    
    args = parser.parse_args()
    
    RECTANGLE_THICKNESS = args.thickness
    USE_COLAB_IMSHOW = args.c
    if USE_COLAB_IMSHOW:
        print(f"Importing cv2_imshow")
        from google.colab.patches import cv2_imshow
        from IPython.display import Image, display
    
    main(args.directory, args.delay, args.max_counter)
    pass