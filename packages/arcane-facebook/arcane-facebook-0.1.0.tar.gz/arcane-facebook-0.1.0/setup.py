# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['facebook_business==5.0.3']

setup_kwargs = {
    'name': 'arcane-facebook',
    'version': '0.1.0',
    'description': 'Helpers to request facebook API',
    'long_description': '# Arcane facebook\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
