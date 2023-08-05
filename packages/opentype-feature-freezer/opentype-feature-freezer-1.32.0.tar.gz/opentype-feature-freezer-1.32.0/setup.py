# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['opentype_feature_freezer']

package_data = \
{'': ['*']}

install_requires = \
['fonttools>=4.0,<5.0']

entry_points = \
{'console_scripts': ['pyftfeatfreeze = opentype_feature_freezer.cli:main']}

setup_kwargs = {
    'name': 'opentype-feature-freezer',
    'version': '1.32.0',
    'description': "Turns OpenType features 'on' by default in a font: reassigns the font's Unicode-to-glyph mapping fo permanently 'freeze' the 1-to-1 substitution features, and creates a new font.",
    'long_description': None,
    'author': 'Adam Twardoch',
    'author_email': 'adam@twardoch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
