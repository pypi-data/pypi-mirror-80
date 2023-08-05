# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icedata',
 'icedata.datasets',
 'icedata.datasets.birds',
 'icedata.datasets.coco',
 'icedata.datasets.coco.tests',
 'icedata.datasets.fridge',
 'icedata.datasets.fridge.tests',
 'icedata.datasets.pennfudan',
 'icedata.datasets.pennfudan.tests',
 'icedata.datasets.pets',
 'icedata.datasets.pets.tests',
 'icedata.datasets.voc',
 'icedata.utils']

package_data = \
{'': ['*'],
 'icedata.datasets.fridge': ['sample_data/odFridgeObjects/annotations/*',
                             'sample_data/odFridgeObjects/images/*'],
 'icedata.datasets.pennfudan': ['sample_data/Annotation/*',
                                'sample_data/PNGImages/*',
                                'sample_data/PedMasks/*'],
 'icedata.datasets.pets': ['images/*',
                           'sample_data/annotations/images/*',
                           'sample_data/annotations/trimaps/*',
                           'sample_data/annotations/xmls/*']}

install_requires = \
['icevision[all]>=0.1.3post2,<0.2.0']

setup_kwargs = {
    'name': 'icedata',
    'version': '0.0.2.post2',
    'description': 'Datasets collection',
    'long_description': None,
    'author': 'Lucas Goulart Vazquez',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
