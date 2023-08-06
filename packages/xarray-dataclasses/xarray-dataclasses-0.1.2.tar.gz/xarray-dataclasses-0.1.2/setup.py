# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_dataclasses']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18,<2.0', 'xarray>=0.15,<0.16']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'xarray-dataclasses',
    'version': '0.1.2',
    'description': 'xarray extension for dataarray classes',
    'long_description': '# xarray-dataclasses\n\n[![PyPI](https://img.shields.io/pypi/v/xarray-dataclasses.svg?label=PyPI&style=flat-square)](https://pypi.org/project/xarray-dataclasses/)\n[![Python](https://img.shields.io/pypi/pyversions/xarray-dataclasses.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/xarray-dataclasses/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/xarray-dataclasses/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/xarray-dataclasses/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nxarray extension for dataarray classes\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/xarray-dataclasses/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
