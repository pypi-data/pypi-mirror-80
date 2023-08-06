# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_tox_test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-tox-test',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Viacheslav Bessonov',
    'author_email': 'viacheslav.bessonov@hilbertteam.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
