# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mylib_mnemos']

package_data = \
{'': ['*']}

install_requires = \
['gensim>=3.8.3,<4.0.0', 'pytest>=6.0.2,<7.0.0']

setup_kwargs = {
    'name': 'mylib-mnemos',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gaëtan Pruvost',
    'author_email': 'gaetan.pruvost@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
