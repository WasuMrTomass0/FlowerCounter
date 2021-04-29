import glob
import cv2
import xmltodict
import argparse


def check_img_sizes_from_xml(dir):
    # Read all xml files in directory
    paths = glob.glob(f"{dir}/*.xml")
    # Show info
    print(f"Found {len(paths)} xml files in {dir}")
    # Prepare dict
    shapes = dict()
    # Read all sizes from xml files:
    for xml_file in paths:
        # Read file
        with open(xml_file, 'r') as token:
            xml = token.read()
        # Convert to dict
        xml = xmltodict.parse(xml)
        # Read size
        img_width  = xml['annotation']['size']['width']
        img_height = xml['annotation']['size']['height']
        img_depth  = xml['annotation']['size']['depth']
        img_size = (img_width, img_height, img_depth)
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
    parser = argparse.ArgumentParser(description="Rescale images")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    args = parser.parse_args()
    check_img_sizes_from_xml(args.directory)
    pass


"""
# def check_img_sizes(dir, img_ext_list):
  # paths = []
  # for ext in img_ext_list:
    # paths += glob.glob(f"{dir}/*.{ext}")
  # print(f"Got {len(paths)} elements in {dir}")
  # shapes = dict()
  # for file in paths:
    # img = cv2.imread(file)
    # shape = img.shape
    # if shape in shapes:
      # shapes[shape] += 1
    # else:
      # shapes[shape] = 1
    # pass
  # for key, value in shapes.items():
    # print(f"\tShape: {key}, \tNum: {value}")
    # pass
  # pass

# img_ext = ["JPG", "png", "jpg", "jpeg"]
# check_img_sizes(f"{TRAINING_PATH}/images/train", img_ext)
# check_img_sizes(f"{TRAINING_PATH}/images/test", img_ext)
"""
