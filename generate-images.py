import os
import math
from pathlib import Path

import numpy
from skimage import (
    color, data, draw, exposure, feature, filters,
    filters, future, graph, io, measure, morphology, novice,
    restoration, segmentation, transform, util
)
from matplotlib import pyplot
import imageio
import ruamel.yaml as yaml


class ImageSaver:
    def __init__ (self, base_path, base_name):
        self.base_path = base_path
        self.base_name = base_name

    def set_base_path (self, base_path):
        self.base_path = base_path
        return self

    def save (self, method_name, input, output):
        method_path = Path(self.base_path, self.base_name, method_name)
        method_path.parent.mkdir(parents=True, exist_ok=True)

        imageio.imwrite(str(method_path) + '_in.png', input)
        imageio.imwrite(str(method_path) + '_out.png', output)

        return self

elements = {
    'disk(5)': morphology.disk(5),
}
defaults = {
    'disk': morphology.disk(5),
    'image_name': 'text_inverted',
    'geometry': (0, 0, 90, 160), # row, col, rows, columns
}

# Alias some image names
data.blank = lambda: numpy.zeros(geo[2:4])
data.text_inverted = lambda: util.invert(data.text())
data.text_bw = lambda: data.bw_text()
data.text_bw_inverted = lambda: util.invert(data.bw_text())

with open('_data/categories.yaml') as stream:
    try:
        categories = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def my_import (components):
    the_module = __import__('.'.join(components))
    for comp in components[1:]:
        the_module = getattr(the_module, comp)
    return the_module

for category in categories:
    module = globals()[category['name']]

    for subcategory in category['children']:
        if subcategory['name']:
            submodule = getattr(module, subcategory['name'])

        saver = ImageSaver(
            base_path = Path(__file__, '../images/generated').resolve(),
            base_name = category['name'] + '/' + subcategory['name']
        )
        for method in subcategory['children']:
            geo = method.get('geometry', defaults['geometry'])
            args = method.get('args', {})
            image_name = args.get('image', defaults['image_name'])
            image_func = getattr(data, image_name)
            selem = args.get('selem')
            if selem:
                args['selem'] = elements.get(selem)


            if category['name'] == 'draw':
                func = getattr(module, method['name'])
                input = data.blank()
                output = data.blank()
                rr, cc = func(**args)
                output[rr, cc] = 1
            else:
                func = getattr(submodule, method['name'])
                args['image'] = image_func()[
                    geo[0]:(geo[0] + geo[2]),
                    geo[1]:(geo[1] + geo[3]),
                ]
                input = args['image']
                output = func(**args)

            saver.save(
                method_name=method['name'],
                input=input,
                output=output,
            )

# rankSaver.save(
#     func=filters.rank.enhance_contrast_percentile,
#     source=text_image,
#     args={
#         'selem': disk5,
#         'p0': 0.2,
#         'p1': 0.8,
#     },
# )
