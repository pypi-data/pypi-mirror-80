# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['layered_config']

package_data = \
{'': ['*']}

extras_require = \
{'munch': ['munch']}

setup_kwargs = {
    'name': 'layered-config',
    'version': '2.0.3',
    'description': 'A tool for managing layered config files!',
    'long_description': None,
    'author': 'Doug Philips',
    'author_email': 'dgou@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jolly-good-toolbelt/layered-config',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
