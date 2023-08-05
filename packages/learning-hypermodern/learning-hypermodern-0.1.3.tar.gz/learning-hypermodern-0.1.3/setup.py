# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['learning_hypermodern']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.8.0,<4.0.0',
 'requests>=2.24.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

entry_points = \
{'console_scripts': ['learning-hypermodern = '
                     'learning_hypermodern.console:main']}

setup_kwargs = {
    'name': 'learning-hypermodern',
    'version': '0.1.3',
    'description': 'The hypermodern Python project',
    'long_description': '# learning-hypermodern\n[![Tests](https://github.com/abstractlyZach/learning-hypermodern/workflows/Tests/badge.svg)](https://github.com/abstractlyZach/learning-hypermodern/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/abstractlyZach/learning-hypermodern/branch/master/graph/badge.svg)](https://codecov.io/gh/abstractlyZach/learning-hypermodern)\n[![PyPI](https://img.shields.io/pypi/v/learning-hypermodern.svg)](https://pypi.org/project/learning-hypermodern/)\n\n\n\nLearning Hypermodern Python through this article: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n',
    'author': 'abstractlyZach',
    'author_email': 'zach3lee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abstractlyZach/learning-hypermodern',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
