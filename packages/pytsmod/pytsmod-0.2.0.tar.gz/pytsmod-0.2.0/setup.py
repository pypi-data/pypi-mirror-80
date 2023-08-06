# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytsmod', 'pytsmod.utils']

package_data = \
{'': ['*']}

install_requires = \
['librosa>=0.8,<0.9',
 'numpy>=1.16.0,<2.0.0',
 'scipy>=1.0.0,<2.0.0',
 'soundfile>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'pytsmod',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Sangeon Yong',
    'author_email': 'koragon2@kaist.ac.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
