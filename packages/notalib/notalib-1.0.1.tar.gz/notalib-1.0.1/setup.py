# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notalib', 'notalib.django', 'notalib.pandas']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.14.0']

setup_kwargs = {
    'name': 'notalib',
    'version': '1.0.1',
    'description': '',
    'long_description': None,
    'author': 'm1kc (Max Musatov)',
    'author_email': 'm1kc@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
