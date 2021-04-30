import os
import glob
import pandas as pd
from WasuLib.xml_image import XMLImage
import xml.etree.ElementTree as ET


def xml_to_csv2(path: str):
    xml_list = []
    xml_paths = glob.glob(path + '/*.xml')
    print(f"Got {len(xml_paths)} in directory {path}")
    for xml_path in xml_paths:
        xml_obj = XMLImage(xml_path=xml_path)
        filename = xml_obj.image_filename
        width = xml_obj.width
        height = xml_obj.height
        for box in xml_obj.boxes_classes:
            value = [filename, width, height, box.label, box.x_min, box.y_min, box.x_max, box.y_max]
            xml_list.append(value)
            pass  # for box
        pass  # for xml_path
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    for folder in ['train', 'test']:
        image_path = os.path.join(os.getcwd(), ('images/' + folder))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(('images/'+folder+'_labels.csv'), index=False)
    print('Successfully converted xml to csv.')


main()
