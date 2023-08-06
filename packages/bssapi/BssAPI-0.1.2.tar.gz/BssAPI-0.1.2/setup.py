# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bssapi',
 'bssapi.api.router',
 'bssapi.api.router.parser',
 'bssapi.core.dbf',
 'bssapi.core.json',
 'bssapi.schemas',
 'bssapi.schemas.http.headers']

package_data = \
{'': ['*']}

install_requires = \
['aioftp>=0.18.0,<0.19.0',
 'attr>=0.3.1,<0.4.0',
 'bssapi-dbfread>=0.1.0,<0.2.0',
 'bssapi-schemas>=0.1.0,<0.2.0',
 'fastapi[all]>=0.61.1,<0.62.0',
 'lz4>=3.1.0,<4.0.0',
 'orjson>=3.3.1,<4.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'python-multipart>=0.0.5,<0.0.6',
 'std-hash>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['bapi = bssapi:app']}

setup_kwargs = {
    'name': 'bssapi',
    'version': '0.1.2',
    'description': 'Функционал перефирийного взаимодействия корпоративной учетной системы BSS',
    'long_description': None,
    'author': 'Anton Rastyazhenko',
    'author_email': 'rastyazhenko.anton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
