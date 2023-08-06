# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bssapi_schemas',
 'bssapi_schemas.odata',
 'bssapi_schemas.odata.InformationRegister',
 'bssapi_schemas.odata.error',
 'bssapi_schemas.odata.mixin']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'bssapi-schemas',
    'version': '0.1.7',
    'description': 'Схемы BSS',
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
