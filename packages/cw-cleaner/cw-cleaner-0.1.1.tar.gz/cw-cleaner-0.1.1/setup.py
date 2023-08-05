# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cw_cleaner']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.62,<2.0.0', 'fire>=0.3.1,<0.4.0', 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['cw-cleaner = cw_cleaner.__main__:main']}

setup_kwargs = {
    'name': 'cw-cleaner',
    'version': '0.1.1',
    'description': 'cli tool to clean and maintain cw logs.',
    'long_description': '# CloudWatch log cleaner\n\ncli tool to clean and maintain cw logs.\n\n```sh\npython3 cw-log-cleaner.py list\npython3 cw-log-cleaner.py table\n```\n',
    'author': 'Nir Adler',
    'author_email': 'me@niradler.com',
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
