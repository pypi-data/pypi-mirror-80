# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['choosem', 'choosem.cli']

package_data = \
{'': ['*'], 'choosem': ['data/*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['choosem = choosem.main:main']}

setup_kwargs = {
    'name': 'choosem',
    'version': '0.1.0',
    'description': 'dropdown picker/launcher for macos',
    'long_description': '# choosem\n\n`choosem` is a [choose] based picker and launcher for macos.\nCurrently these functionalities are available:\n\n* Insert select character from character dictionaries\n* Focus [Yabai] program\n* Launch programs\n\n# install\n\nfor python 3.6+:\n```\n$ pip install --user choosem \n...\n$ choosem --help\nUsage: choosem [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  insert  insert character into active window\n  yabai   control yabai windows manager\n```\n\n## Known issues\n\n`insert` command might stop working, for this accessibility permission needs to be disabled and then enabled again.\n\n[choose]: https://github.com/chipsenkbeil/choose\n\n\n',
    'author': 'Bernardas Alisauskas',
    'author_email': 'bernardas.alisauskas@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Granitosaurus/choosem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
