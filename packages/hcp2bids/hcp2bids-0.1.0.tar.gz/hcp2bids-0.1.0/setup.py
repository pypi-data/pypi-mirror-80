# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hcp2bids', 'hcp2bids.subjects']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.15.1,<2.0.0', 'pybids>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'hcp2bids',
    'version': '0.1.0',
    'description': 'For downloading and converting HCP1200 data into BIDS spec.',
    'long_description': None,
    'author': 'j1c',
    'author_email': 'jaewonc78@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
