#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
import logging
import numpy as np
from ._base import *

try:
    import yaml
except ImportError:
    yaml = None

__all__ = ["YamlParser"]
log = logging.getLogger(__name__)


class YamlParser(DetectionParser):
    """
    This parser generates a lightweight human readable detection format.
    With only one file for the entire dataset, this format will save you precious HDD space and will also be parsed faster.

    Keyword Args:
        precision (integer): The number of decimals for the coordinates; Default **None** (save as int)

    Example:
        >>> detections.yaml
            img1:
              car:
                - coords: [x,y,w,h]
                  score: 56.76
              person:
                - coords: [x,y,w,h]
                  id: 1
                  score: 90.1294132
                - coords: [x,y,w,h]
                  id: 2
                  score: 12.120
            img2:
              car:
                - coords: [x,y,w,h]
                  score: 50
    """
    parser_type = ParserType.SINGLE_FILE
    serialize_group = 'image'
    extension = '.yaml'

    def __init__(self, precision=None):
        if yaml is None:
            raise ImportError('Pyyaml package not found. Please install it in order to use this parser!')

        super().__init__()
        self.precision = precision

    def serialize(self, df):
        result = {}

        for row in df.itertuples():
            box = {
                'coords': [round(row.x_top_left, self.precision), round(row.y_top_left, self.precision),
                           round(row.width, self.precision), round(row.height, self.precision)],
                'score': row.confidence*100,
            }
            if not np.isnan(row.id):
                box['id'] = int(row.id)

            class_label = row.class_label if row.class_label != '' else '?'
            if class_label not in result:
                result[class_label] = [box]
            else:
                result[class_label].append(box)

        return yaml.dump({df.name: result}, default_flow_style=None)

    def deserialize(self, rawdata, file_id=None):
        yml_obj = yaml.safe_load(rawdata)

        for file_id in yml_obj:
            self.append_image(file_id)
            if yml_obj is not None:
                for class_label, annos in yml_obj[file_id].items():
                    for anno in annos:
                        data = dict(
                            class_label='' if class_label == '?' else class_label,
                            x_top_left=float(anno['coords'][0]),
                            y_top_left=(anno['coords'][1]),
                            width=float(anno['coords'][2]),
                            height=float(anno['coords'][3]),
                            confidence=anno['score'] / 100,
                        )

                        if 'id' in anno:
                            data['id'] = anno['id']

                        self.append(file_id, **data)
