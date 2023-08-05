# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_accessors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xarray-accessors',
    'version': '0.1.0',
    'description': 'xarray extension for dataarray accessors',
    'long_description': '# xarray-accessors\n\n[![PyPI](https://img.shields.io/pypi/v/xarray-accessors.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/xarray-accessors/)\n[![Python](https://img.shields.io/pypi/pyversions/xarray-accessors.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/xarray-accessors/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/xarray-accessors/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/xarray-accessors/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nxarray extension for dataarray accessors\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/xarray-accessors/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
