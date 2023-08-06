# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyap', 'pyap.packages', 'pyap.source_CA', 'pyap.source_GB', 'pyap.source_US']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyap',
    'version': '0.3.0',
    'description': 'Pyap is an MIT Licensed text processing library, written in Python, for detecting and parsing addresses. Currently it supports USA, Canadian and British addresses.',
    'long_description': None,
    'author': 'Vladimir Goncharov',
    'author_email': 'vladimarius@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
