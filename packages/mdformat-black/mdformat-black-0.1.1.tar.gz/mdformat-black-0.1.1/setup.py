# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_black']

package_data = \
{'': ['*']}

install_requires = \
['black', 'mdformat>=0.3.0']

entry_points = \
{'mdformat.codeformatter': ['python = mdformat_black:format_python']}

setup_kwargs = {
    'name': 'mdformat-black',
    'version': '0.1.1',
    'description': 'Mdformat plugin to Blacken Python code blocks',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-black/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-black/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)\n[![PyPI version](https://badge.fury.io/py/mdformat-black.svg)](<https://badge.fury.io/py/mdformat-black>)\n\n# mdformat-black\n> Mdformat plugin to Blacken Python code blocks\n\n## Description\nmdformat-black is an [mdformat](https://github.com/executablebooks/mdformat) plugin\nthat makes mdformat format Python code blocks with [Black](https://github.com/psf/black).\n## Usage\nInstall with:\n```bash\npip install mdformat-black\n```\n\nWhen using mdformat on the command line, Black formatting will be automatically enabled after install.\n\nWhen using mdformat Python API, code formatting for Python will have to be enabled explicitly:\n````python\nimport mdformat\n\nunformatted = "```python\\n\'\'\'black converts quotes\'\'\'\\n```\\n"\nformatted = mdformat.text(unformatted, codeformatters={"python"})\nassert formatted == \'```python\\n"""black converts quotes"""\\n```\\n\'\n````\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-black',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
