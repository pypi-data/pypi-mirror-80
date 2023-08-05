# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['git_cu']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['git-cu = git_cu.main:main']}

setup_kwargs = {
    'name': 'git-cu',
    'version': '0.3.0',
    'description': 'git-cu helps keep your local git repositories organised by cloning them into a directory structure based on their URL.',
    'long_description': None,
    'author': 'Vasili Revelas',
    'author_email': 'vasili.revelas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
