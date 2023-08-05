# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pw']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'colorama>=0.4.3,<0.5.0', 'pyperclip>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['pw = pw.__main__:pw']}

setup_kwargs = {
    'name': 'pw',
    'version': '0.13.0',
    'description': 'Search in GPG-encrypted password file.',
    'long_description': '# pw [![Build Status](https://travis-ci.org/catch22/pw.svg?branch=master)](https://travis-ci.org/catch22/pw) [![Latest Version](https://img.shields.io/pypi/v/pw.svg)](https://pypi.python.org/pypi/pw/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/pw.svg)](https://pypi.python.org/pypi/pw/)\n\n\n`pw` is a Python tool to search in a GPG-encrypted password database.\n\n```\nUsage: pw [OPTIONS] [USER@][KEY] [USER]\n\n  Search for USER and KEY in GPG-encrypted password file.\n\nOptions:\n  -C, --copy       Display account information, but copy password to clipboard (default mode).\n  -E, --echo       Display account information as well as password in plaintext (alternative mode).\n  -R, --raw        Only display password in plaintext (alternative mode).\n  -S, --strict     Fail unless precisely a single result has been found.\n  -U, --user       Copy or display username instead of password.\n  -f, --file PATH  Path to password file.\n  --edit           Launch editor to edit password database and exit.\n  --gen            Generate a random password and exit.\n  --version        Show the version and exit.\n  --help           Show this message and exit.\n```\n\n\n## Installation\n\nTo install `pw`, simply run:\n\n```bash\n$ pip install pw\n```\n',
    'author': 'Michael Walter',
    'author_email': 'michael.walter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/catch22/pw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
