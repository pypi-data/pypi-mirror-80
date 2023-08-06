# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_sparklines']

package_data = \
{'': ['*']}

install_requires = \
['rich>=7.1.0,<8.0.0', 'sparklines>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'rich-sparklines',
    'version': '0.1.4',
    'description': 'Integrate rich and sparklines libraries',
    'long_description': None,
    'author': 'Elliana',
    'author_email': 'me@mause.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
