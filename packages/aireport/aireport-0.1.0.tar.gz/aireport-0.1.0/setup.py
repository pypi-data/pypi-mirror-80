# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['aireport']
install_requires = \
['black>=19.10b0,<20.0', 'numpy', 'pandas>=1.0.5,<2.0.0']

setup_kwargs = {
    'name': 'aireport',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'None',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
