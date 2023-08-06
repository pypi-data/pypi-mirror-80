# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zql']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zql',
    'version': '0.0.1',
    'description': 'zQL: a SQL builder based on JSON',
    'long_description': None,
    'author': 'Anthony Leontiev',
    'author_email': 'ant@devlt.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
