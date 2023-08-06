# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imagelab']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17.2,<2.0.0',
 'opencv-contrib-python>=4.4.0,<5.0.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'imagelab',
    'version': '0.1.0',
    'description': 'This package is DTU Compute imagelab SDK for research in image analysis, computer vision, and computational imaging.',
    'long_description': None,
    'author': 'Søren K. S. Gregersen',
    'author_email': 'sorgre@dtu.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
