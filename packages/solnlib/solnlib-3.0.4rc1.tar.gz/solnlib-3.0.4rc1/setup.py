# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solnlib', 'solnlib.modular_input']

package_data = \
{'': ['*']}

install_requires = \
['future>=0,<1',
 'requests>=2.24,<3.0',
 'schematics>=2.1,<3.0',
 'six',
 'sortedcontainers>=2.2,<3.0',
 'splunk-sdk>=1.6,<2.0']

setup_kwargs = {
    'name': 'solnlib',
    'version': '3.0.4rc1',
    'description': 'The Splunk Software Development Kit for Splunk Solutions',
    'long_description': None,
    'author': 'Splunk',
    'author_email': 'addonfactory@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
