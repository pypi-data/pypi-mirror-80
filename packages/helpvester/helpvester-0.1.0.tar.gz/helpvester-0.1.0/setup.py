# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helpvester']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'helpvester',
    'version': '0.1.0',
    'description': 'Utility for harvesting program parameter descriptions from executables',
    'long_description': None,
    'author': 'Pawel Zukowski',
    'author_email': 'p.z.idlecode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
