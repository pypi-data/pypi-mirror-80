# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_config']

package_data = \
{'': ['*']}

install_requires = \
['mdformat>=0.1.2', 'toml>=0.10.0']

entry_points = \
{'mdformat.codeformatter': ['json = mdformat_config:format_json',
                            'toml = mdformat_config:format_toml']}

setup_kwargs = {
    'name': 'mdformat-config',
    'version': '0.1.0',
    'description': 'Mdformat plugin to beautify configuration and data-serialization formats',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-config/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-config/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)\n[![PyPI version](https://badge.fury.io/py/mdformat-config.svg)](<https://badge.fury.io/py/mdformat-config>)\n\n# mdformat-config\n> Mdformat plugin to beautify configuration and data-serialization formats\n\n## Description\nmdformat-config is an [mdformat](https://github.com/executablebooks/mdformat) plugin\nthat makes mdformat beautify configuration and data-serialization formats.\nCurrently supported formats are JSON and TOML.\n\n## Usage\nInstall with:\n```console\npip install mdformat-config\n```\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
