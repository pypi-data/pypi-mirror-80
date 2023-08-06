# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geok']

package_data = \
{'': ['*']}

install_requires = \
['arcgis>=1.8.2,<2.0.0', 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'geok',
    'version': '0.2.0a0',
    'description': 'pydantic validation for Esri geometries.',
    'long_description': None,
    'author': 'Samuel Cook',
    'author_email': 'scook@esri.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
