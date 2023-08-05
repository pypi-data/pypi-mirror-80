# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kerassurgeon', 'kerassurgeon._utils', 'kerassurgeon.examples', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.7.0,<2.0.0',
 'keras[standalone-keras]>=2.4.3,<3.0.0',
 'pandas[examples]>=1.1.2,<2.0.0',
 'pillow[examples]>=7.2.0,<8.0.0',
 'pytest[test]>=6.0.2,<7.0.0',
 'tensorflow>=2.0,<3.0']

setup_kwargs = {
    'name': 'kerassurgeon',
    'version': '0.2.0',
    'description': 'A library for performing network surgery on trained Keras models. Useful for deep neural network pruning.',
    'long_description': None,
    'author': 'Ben Whetton',
    'author_email': 'ben.whetton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
