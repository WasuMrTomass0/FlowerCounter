import os.path
import cv2
import glob
import xmltodict
import platform
from copy import deepcopy

SLASH = '\\' if platform.system() == 'Windows' else '/'
print(f"Using '{SLASH}' symbol - system is '{platform.system()}'")

# Prepare image
MODEL_INPUT = 1024
IMAGE_INPUT = MODEL_INPUT * 6
P_SHAPE_OUT = (IMAGE_INPUT, IMAGE_INPUT, 3)

# Divide image
D_SPLIT_INFO = (IMAGE_INPUT//MODEL_INPUT, IMAGE_INPUT//MODEL_INPUT)  # Na ile dzielić każdą z osi

DO_NOT_SHOW = False

# Summary
print(f"MODEL_INPUT {MODEL_INPUT} - rozmiar wyciętego fragmentu zdjęcia")
print(f"P_SHAPE_OUT {P_SHAPE_OUT} - Do tej rozdzielczości skalujemy zdjęcie, zanim zostanie ono podzielone")
print(f"D_SPLIT_INFO {D_SPLIT_INFO}")


def prepare_img(image, b_boxes, method=0):
    if method == 0:  # Resize
        def rescale_coordinate(str_coordinate, scale):
            return int(int(str_coordinate) * scale)
        h_old, w_old = image.shape[:2]
        h_new, w_new = P_SHAPE_OUT[:2]
        x_scale = w_new / w_old
        y_scale = h_new / h_old
        for obj in b_boxes:
            obj['bndbox']['xmin'] = rescale_coordinate(obj['bndbox']['xmin'], x_scale)
            obj['bndbox']['xmax'] = rescale_coordinate(obj['bndbox']['xmax'], x_scale)
            obj['bndbox']['ymin'] = rescale_coordinate(obj['bndbox']['ymin'], y_scale)
            obj['bndbox']['ymax'] = rescale_coordinate(obj['bndbox']['ymax'], y_scale)
            pass
        return cv2.resize(image, P_SHAPE_OUT[:2]), b_boxes
    raise NotImplemented


def divide_img(image, b_boxes):
    # shape_original = image.shape
    # height_original = shape_original[0] // D_SPLIT_INFO[0]
    # width_original = shape_original[1] // D_SPLIT_INFO[1]

    image, b_boxes = prepare_img(image, b_boxes)
    shape_prepared = image.shape
    h = shape_prepared[0] // D_SPLIT_INFO[0]
    w = shape_prepared[1] // D_SPLIT_INFO[1]

    draw_bounding_boxes(image, b_boxes, title='resized')

    # divided_images = [[None for _1 in range(D_SPLIT_INFO[0])] for _2 in range(D_SPLIT_INFO[1])]
    # divided_boxes = [[list() for _1 in range(D_SPLIT_INFO[0])] for _2 in range(D_SPLIT_INFO[1])]
    divided_boxes = list()
    divided_images = list()
    for h_index in range(D_SPLIT_INFO[0]):
        for w_index in range(D_SPLIT_INFO[1]):
            divided_boxes.append([])
            h_start = h_index * h
            h_end = h_start + h
            w_start = w_index * w
            w_end = w_start + w

            sub_image = image[h_start: h_end, w_start: w_end]
            divided_images.append(sub_image)

            # sub_image = image[h_index * h: (h_index + 1) * h, w_index * w: (w_index + 1) * w]
            # divided_images[h_index][w_index] = sub_image

            # Calc centre of mass
            for box in b_boxes:
                x_min = int(box['bndbox']['xmin'])
                x_max = int(box['bndbox']['xmax'])
                y_min = int(box['bndbox']['ymin'])
                y_max = int(box['bndbox']['ymax'])
                x = (x_min + x_max) // 2
                y = (y_min + y_max) // 2
                if not (h_start <= y < h_end and w_start <= x < w_end):
                    continue
                class_name = box['name']

                # print(f"{h_start} <= {y} < {h_end} and {w_start} <= {x} < {w_end}")
                # print(f"({x_min}, {x_max}, {y_min}, {y_max}, {class_name})")
                y_min = max(0, y_min - h_start)
                y_max = min(y_max, y_max - h_start)
                x_min = max(0, x_min - w_start)
                x_max = min(x_max, x_max - w_start)
                # print(f"({x_min}, {x_max}, {y_min}, {y_max}, {class_name})\n")
                divided_boxes[-1].append(
                    (x_min, x_max, y_min, y_max, class_name)
                )
                pass
            pass
        pass
    return divided_images, divided_boxes


def draw_bounding_boxes(image, b_boxes, delay=0, title='draw_bounding_boxes'):
    image = deepcopy(image)
    for box in b_boxes:
        color = (255, 0, 0)
        if type(box) is tuple:
            # (x_min, x_max, y_min, y_max, class_name)
            cv2.rectangle(
                image,
                (box[0], box[2]),
                (box[1], box[3]),
                color
            )
            pass
        elif type(box) in (xmltodict.OrderedDict, dict):
            cv2.rectangle(
                image,
                (int(box['bndbox']['xmin']), int(box['bndbox']['ymin'])),
                (int(box['bndbox']['xmax']), int(box['bndbox']['ymax'])),
                color
            )
            pass
    if not DO_NOT_SHOW:
        cv2.imshow(title, image)
        cv2.waitKey(delay)
    pass


def generate_xml(folder_name, file_name, file_path, img_shape, b_boxes):
    height, width = img_shape[:2]
    depth = img_shape[2] if len(img_shape) >= 2 else 1
    obj_list = []
    for elem in b_boxes:
        objects_text = '\n'.join([
            f"	<object>",
            f"		<name>{elem[4]}</name>",
            f"		<pose>Unspecified</pose>",
            f"		<truncated>0</truncated>",
            f"		<difficult>0</difficult>",
            f"		<bndbox>",
            f"			<xmin>{elem[0]}</xmin>",
            f"			<ymin>{elem[2]}</ymin>",
            f"			<xmax>{elem[1]}</xmax>",
            f"			<ymax>{elem[3]}</ymax>",
            f"		</bndbox>",
            f"	</object>"
        ])
        obj_list.append(objects_text)
        pass
    objects_text = '\n'.join(obj_list)
    xml_text = '\n'.join([
        f"<annotation>",
        f"	<folder>{folder_name}</folder>",
        f"	<filename>{file_name}</filename>",
        f"	<path>{file_path}</path>",
        f"	<source>",
        f"		<database>Unknown</database>",
        f"	</source>",
        f"	<size>",
        f"		<width>{width}</width>",
        f"		<height>{height}</height>",
        f"		<depth>{depth}</depth>",
        f"	</size>",
        f"	<segmented>0</segmented>",
        f"	{objects_text}",
        f"</annotation>"
    ])
    return xml_text


with open('xml_template.txt', 'r') as token:
    XML_TEMPLATE = token.read()
with open('xml_object_template.txt', 'r') as token:
    OBJECT_TEMPLATE = token.read()


def save_data(xml_file_path, image_name, images, b_boxes):
    if len(images) != len(b_boxes):
        raise ValueError

    for a in range(len(images)):
        # Save image
        image_file_name = image_name.replace('.', f'_{a}.')
        image_file_path = os.path.join(f'images{SLASH}test', image_file_name)
        cv2.imwrite(image_file_path, images[a])

        # Create xml_dict
        xml = generate_xml('folder', image_file_name, image_file_path, P_SHAPE_OUT, b_boxes[a])
        # Save resized data into xml file
        xml_file_name = xml_file_path.replace('.', f'_{a}.')
        with open(os.path.join(f'images{SLASH}test', xml_file_name.split(SLASH)[-1]), 'w') as _token:
            _token.write(xml)
        pass
    pass


xml_paths = glob.glob("images/*.xml")

for xml_path in xml_paths:
    # Read xml file
    with open(xml_path, 'r') as token:
        xml_dict = xmltodict.parse(token.read())

    # Read image file name
    img_name = xml_dict['annotation']['filename']
    img_path = xml_path.split('.')[0] + '.' + img_name.split('.')[-1]

    # Read image
    img = cv2.imread(img_path)

    # Read BBoxes info
    boxes = xml_dict['annotation']['object']
    # Single bounding box in image is stored differently than multiple bounding boxes
    if type(boxes) != list:
        boxes = [boxes]

    # Print info
    print(f"{img.shape}, {img_path} from {xml_path} - got {len(boxes)} boxes")

    # Divide image
    split_images, split_boxes = divide_img(img, boxes)

    # Save
    save_data(xml_path, img_name, split_images, split_boxes)

    pass

img_paths = glob.glob('images/test/*.JPG')
for img_path in img_paths:
    img = cv2.imread(img_path)

    with open(img_path.replace('.JPG', '.xml'), 'r') as token:
        xml_dict = xmltodict.parse(token.read())
    if 'object' not in xml_dict['annotation']:
        boxes = []
    else:
        boxes = xml_dict['annotation']['object']
        if type(boxes) != list:
            boxes = [boxes]
    draw_bounding_boxes(img, boxes, delay=250, title='divided')
    pass
