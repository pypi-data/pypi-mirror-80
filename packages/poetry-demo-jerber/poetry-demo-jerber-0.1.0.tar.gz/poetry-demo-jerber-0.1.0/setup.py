# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_jerber', 'poetry_demo_jerber.Models', 'poetry_demo_jerber.Outer']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'poetry-demo-jerber',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
