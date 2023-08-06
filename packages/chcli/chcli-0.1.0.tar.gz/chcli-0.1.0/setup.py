# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chcli', 'chcli.grammar']

package_data = \
{'': ['*']}

install_requires = \
['antlr4-python3-runtime',
 'async_lru',
 'asynch',
 'click',
 'prompt_toolkit',
 'rich',
 'sqlparse']

entry_points = \
{'console_scripts': ['chcli = chcli.cli:main']}

setup_kwargs = {
    'name': 'chcli',
    'version': '0.1.0',
    'description': 'A Terminal Client for ClickHouse with AutoCompletion and Syntax Highlighting.',
    'long_description': '# chcli\n\nA Terminal Client for ClickHouse with AutoCompletion and Syntax Highlighting.\n\nThis project is inspired by [mycli](https://github.com/dbcli/mycli).\n\n## Features\n\n`chcli` is written using [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) and [antlr4](https://pypi.org/project/antlr4-python3-runtime/) with [grammar](https://github.com/ClickHouse/ClickHouse/tree/master/utils/grammar).\n\n- Auto-completion as you type for SQL keywords as well as tables, views and columns in the database.\n- Syntax highlighting using `Pygments`.\n- Pretty prints tabular data.\n\n## Install\n\nYou can install just by pip.\n\n```shell script\n> pip install chcli\n```\n\n## Usage\n\n```shell script\n> chcli --help\nUsage: chcli [OPTIONS]\n\n  A Terminal Client for ClickHouse with AutoCompletion and Syntax\n  Highlighting.\n\nOptions:\n  -v, --version       Show the version and exit.\n  -h, --host TEXT     ClickHouse server host.  [default: 127.0.0.1]\n  -p, --port INTEGER  ClickHouse server port.  [default: 9000]\n  -u, --user TEXT     ClickHouse server user.  [default: default]\n  --password TEXT     ClickHouse server password.  [default: ]\n  --help              Show this message and exit.\n```\n\n## License\n\nThis project is licensed under the [Apache-2.0](https://github.com/long2ice/chcli/blob/master/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/chcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
