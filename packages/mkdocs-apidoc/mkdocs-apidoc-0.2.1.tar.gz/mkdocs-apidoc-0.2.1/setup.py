# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_apidoc']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.2.0,<21.0.0',
 'jinja2>=2.10,<3.0',
 'mkdocs>=1.1,<2.0',
 'numpydoc>=0.9.2,<0.10.0']

entry_points = \
{'mkdocs.plugins': ['mkdocs_apidoc = mkdocs_apidoc.plugin:ApiDocPlugin']}

setup_kwargs = {
    'name': 'mkdocs-apidoc',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Evan',
    'author_email': 'evanmcurtin@gmail.com',
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
