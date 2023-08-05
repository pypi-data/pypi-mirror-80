# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jure']

package_data = \
{'': ['*']}

install_requires = \
['jupytext>=1.5.2,<2.0.0',
 'loguru>=0.5.2,<0.6.0',
 'pytest>=6.0.1,<7.0.0',
 'selenium>=3.141.0,<4.0.0',
 'watchdog>=0.10.3,<0.11.0']

entry_points = \
{'console_scripts': ['jure = jure.main:main']}

setup_kwargs = {
    'name': 'jure',
    'version': '0.1.2',
    'description': 'An utility that extends Jupytext. Allows to auto-refresh browser when source file is changed.',
    'long_description': '# Jupyter Browser Reload\n\nConvenience tool around Jupytext to automatically reload browser\nwhen source file is changed. \n\n## Installation\n\n```\npip install jure\n```',
    'author': 'Dmitry Lipin',
    'author_email': 'd.lipin@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
