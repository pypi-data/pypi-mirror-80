# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colour_sort']

package_data = \
{'': ['*']}

install_requires = \
['importlib_resources>=1.0,<2.0', 'numpy>=1.17,<2.0', 'pillow>=6.2,<7.0', 'sklearn', 'scikit-image>=0.17.2,<1.0.0',
 'opencv-python>=4.2.0.34,<5.0' ]

entry_points = \
{'console_scripts': ['colour = colour_sort:cli.run']}

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup_kwargs = {
    'name': 'colour-sort',
    'version': '0.1.4.a1',
    'description': 'A tool to generate images using all rgb colours with no duplicates.',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'author': 'David Buckley',
    'author_email': 'david-pypi@davidbuckley.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/buckley-w-david/colour_sort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.7',
}


setup(**setup_kwargs)
