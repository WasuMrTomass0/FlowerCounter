from WasuLib.trace import Trace


class BBox:
    """
    Class representing bounding box
    """
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int, label: str):
        self.x_min = min(int(x_min), int(x_max))
        self.y_min = min(int(y_min), int(y_max))
        self.x_max = max(int(x_min), int(x_max))
        self.y_max = max(int(y_min), int(y_max))
        self.label = str(label)
        self._calculate()
        pass

    def _calculate(self):
        self.x_centre = (self.x_max + self.x_min) // 2
        self.y_centre = (self.y_max + self.y_min) // 2
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
        self.area = self.width * self.height

        self.is_correct = self.width > 0 and self.height > 0
        if not self.is_correct:
            Trace(f"Invalid BBox {str(self)}", Trace.TRACE_WARNING, __file__, self._calculate.__name__)
        pass  # def _calculate

    def __str__(self):
        return f"{self.label} min ({self.x_min}, {self.y_min}) max({self.x_max}, {self.y_max})"

    def update(self, x_min: int, y_min: int, x_max: int, y_max: int, label: str):
        self.x_min = int(x_min)
        self.y_min = int(y_min)
        self.x_max = int(x_max)
        self.y_max = int(y_max)
        self.label = str(label)
        self._calculate()
        pass

    @staticmethod
    def from_dict(xml_dict: dict):
        """
        Create BBox object from xml dict (single bounding box)
        :param xml_dict: Single bounding box as dictionary
        :return: BBox object
        """
        x_min = int(xml_dict['bndbox']['xmin'])
        y_min = int(xml_dict['bndbox']['ymin'])
        x_max = int(xml_dict['bndbox']['xmax'])
        y_max = int(xml_dict['bndbox']['ymax'])
        label = str(xml_dict['name'])
        return BBox(x_min, y_min, x_max, y_max, label)

    def to_xml_text(self) -> str:
        """
        Generate xml text
        :return:
        """
        xml_text = '\n'.join([
            f"	<object>",
            f"		<name>{self.label}</name>",
            f"		<pose>Unspecified</pose>",
            f"		<truncated>0</truncated>",
            f"		<difficult>0</difficult>",
            f"		<bndbox>",
            f"			<xmin>{self.x_min}</xmin>",
            f"			<ymin>{self.y_min}</ymin>",
            f"			<xmax>{self.x_max}</xmax>",
            f"			<ymax>{self.y_max}</ymax>",
            f"		</bndbox>",
            f"	</object>"
        ])
        return xml_text
    pass
