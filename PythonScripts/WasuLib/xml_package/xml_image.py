import xmltodict
import os
from copy import deepcopy
from typing import List
from WasuLib.bounding_box import BBox
from WasuLib.trace import Trace


class XMLImage:
    """
    Class used as an interface to xml file created by labelImg
    """
    def __init__(self, xml_text: str = None, xml_path: str = None):
        if not xml_text and not xml_path:
            raise ValueError('Pass the xml text or path to xml file')
        if xml_path:
            if not os.path.isfile(xml_path):
                raise ValueError(f'No such xml file: {xml_path}')
            with open(xml_path, 'r') as token:
                xml_text = token.read()
            pass  # if xml_path

        self.xml_text = xml_text
        self.xml_path = xml_path
        data = xmltodict.parse(xml_text)

        self.folder = str(data['annotation']['folder'])
        self.image_filename = str(data['annotation']['filename'])
        self.path = str(data['annotation']['path'])
        self.height = int(data['annotation']['size']['height'])
        self.width = int(data['annotation']['size']['width'])
        self.depth = int(data['annotation']['size']['depth'])

        self._boxes_dicts = data['annotation']['object'] if 'object' in data['annotation'] else list()
        if type(self._boxes_dicts) != list:
            self._boxes_dicts = [self._boxes_dicts]

        self.boxes_classes = list()
        for elem in self._boxes_dicts:
            self.boxes_classes.append(BBox.from_dict(elem))

        pass  # def __init__

    def image_path(self) -> str:
        img_ext = self.image_filename.split('.')[-1]
        return self.xml_path.replace(".xml", f".{img_ext}")

    def save(self, file_path: str = None, update_xml: bool = True):
        file_path = file_path if file_path else self.xml_path
        if update_xml:
            self.update_xml_text()
        with open(file_path, 'w') as token:
            token.write(self.xml_text)
        pass

    @staticmethod
    def create_xml_text(folder: str, image_filename: str, path: str, width: int, height: int, depth: int,
                        boxes_classes: List[BBox]) -> str:
        objects_text = '\n'.join([elem.to_xml_text() for elem in boxes_classes])
        xml_text = '\n'.join([
            f"<annotation>",
            f"	<folder>{folder}</folder>",
            f"	<filename>{image_filename}</filename>",
            f"	<path>{path}</path>",
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

    def update_xml_text(self) -> None:
        self.xml_text = self.create_xml_text(
            folder=self.folder,
            image_filename=self.image_filename,
            path=self.path,
            width=self.width,
            height=self.height,
            depth=self.depth,
            boxes_classes=self.boxes_classes
        )
        pass  # def update_xml_text

    # Stage prepare

    def resize(self, shape2d):
        obj = deepcopy(self)
        h_new, w_new = shape2d
        x_scale = w_new / obj.width
        y_scale = h_new / obj.height
        # Update image dimension
        obj.height = shape2d[0]
        obj.width = shape2d[1]
        # Rescale each BBox
        for elem in obj.boxes_classes:
            elem.update(elem.x_min * x_scale, elem.y_min * y_scale,
                        elem.x_max * x_scale, elem.y_max * y_scale, elem.label)
            pass  # for elem
        # Update xml text
        obj.update_xml_text()
        return obj

    def black_bars(self, shape2d):
        obj = deepcopy(self)
        # Update image dimension
        obj.height = shape2d[0]
        obj.width = shape2d[1]
        # Update xml text
        obj.update_xml_text()
        return obj

    # Stage divide

    def _divide_boxes(self, shape2d) -> List:
        h_sub, w_sub = shape2d
        h_img = self.height
        w_img = self.width
        no_h = h_img // h_sub
        no_w = w_img // w_sub

        ret = [list() for _ in range(no_h * no_w)]
        for box in self.boxes_classes:
            h_index = box.y_centre // h_sub
            w_index = box.x_centre // w_sub

            h_start = h_index * h_sub
            w_start = w_index * w_sub

            x_min = max(0, box.x_min - w_start)
            y_min = max(0, box.y_min - h_start)
            x_max = min(w_sub, box.x_max - w_start)
            y_max = min(h_sub, box.y_max - h_start)

            b = BBox(x_min, y_min, x_max, y_max, box.label)
            ret[h_index * no_w + w_index] += [b]

            # Trace(f"Centre {(box.x_centre, box.y_centre)}, Index hw {(h_index, w_index)}, "
            #       f"Start hw {(h_start, w_start)}, \nbox {box}  ->  b {b}",
            #       Trace.TRACE_DEBUG, __file__, self.divide.__name__)
            pass
        return ret

    def divide(self, shape2d) -> List:
        # Divide boxes
        sub_boxes = self._divide_boxes(shape2d)
        # Create XMLImages
        sub_xmls = list()
        for boxes_list in sub_boxes:
            xml_text = self.create_xml_text(
                folder=self.folder,
                image_filename=self.image_filename,
                path=self.path,
                width=shape2d[1],
                height=shape2d[0],
                depth=self.depth,
                boxes_classes=boxes_list
            )
            xml_obj = XMLImage(xml_text=xml_text)
            sub_xmls.append(xml_obj)
            pass

        Trace(f"From {len(self.boxes_classes)} to {sum([len(elem) for elem in sub_boxes])}"
              f" - {[len(elem) for elem in sub_boxes]} . File {self.image_filename}",
              Trace.TRACE_DEBUG, __file__, self.divide.__name__)

        return sub_xmls

    pass  # class XMLImage
