# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notify_me_tool']

package_data = \
{'': ['*']}

install_requires = \
['pluggy>=0.13.1,<0.14.0', 'singleton-decorator>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['notify-me = notify_me_tool.host:main']}

setup_kwargs = {
    'name': 'notify-me-tool',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'John Hossler',
    'author_email': 'john.m.hossler@gmail.com',
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
