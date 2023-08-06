# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['luts']

package_data = \
{'': ['*']}

install_requires = \
['netcdf4>=1.5.4,<2.0.0',
 'numpy>=1.19.2,<2.0.0',
 'scipy>=1.5.2,<2.0.0',
 'xarray>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'luts',
    'version': '1.0.0',
    'description': 'Multidimensional labeled arrays and datasets in Python, similar to xarray.',
    'long_description': None,
    'author': 'François Steinmetz',
    'author_email': 'fs@hygeos.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
