# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane', 'arcane.notification']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.7,<3.0']

setup_kwargs = {
    'name': 'arcane-notification',
    'version': '0.1.5',
    'description': 'Defines notification tools',
    'long_description': '# Arcane notification\n',
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
