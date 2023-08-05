# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['std_hash']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.3.1,<4.0.0', 'pydantic>=1.6.1,<2.0.0', 'typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'std-hash',
    'version': '0.1.2',
    'description': 'Тупое хеширование объектов',
    'long_description': None,
    'author': 'Anton Rastyazhenko',
    'author_email': 'rastyazhenko.anton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
