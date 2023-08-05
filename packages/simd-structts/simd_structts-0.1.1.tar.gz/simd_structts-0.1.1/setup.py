# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['simd_structts', 'simd_structts.backends', 'simd_structts.backends.simdkalman']

package_data = \
{'': ['*']}

install_requires = \
['simdkalman==1.0.1', 'statsmodels>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'simd-structts',
    'version': '0.1.1',
    'description': 'SIMD implementation of the StructTS/Unobserved Components model',
    'long_description': None,
    'author': 'Vladimir Shulyak',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
