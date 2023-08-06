# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbjuniper']

package_data = \
{'': ['*']}

install_requires = \
['markdown>=3.2.2,<4.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['nbjuniper = entry:main']}

setup_kwargs = {
    'name': 'nbjuniper',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Michael Ashton',
    'author_email': 'mashton@ufl.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
