# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytsmod', 'pytsmod..ipynb_checkpoints', 'pytsmod.utils']

package_data = \
{'': ['*']}

install_requires = \
['data-science-types>=0.2.17,<0.3.0',
 'nptyping>=1.3.0,<2.0.0',
 'numpy>=1.19.2,<2.0.0']

setup_kwargs = {
    'name': 'pytsmod',
    'version': '0.1.0',
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
