# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commanderbot_lib',
 'commanderbot_lib.bot',
 'commanderbot_lib.bot.abc',
 'commanderbot_lib.database',
 'commanderbot_lib.database.abc',
 'commanderbot_lib.guild_state',
 'commanderbot_lib.guild_state.abc',
 'commanderbot_lib.mixins',
 'commanderbot_lib.options',
 'commanderbot_lib.options.abc',
 'commanderbot_lib.state',
 'commanderbot_lib.state.abc',
 'commanderbot_lib.store',
 'commanderbot_lib.store.abc']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.4.1,<2.0.0']

extras_require = \
{'log-colors': ['colorama>=0.4.3,<0.5.0', 'colorlog>=4.2.1,<5.0.0'],
 'yaml': ['pyyaml>=5.3.1,<6.0.0']}

setup_kwargs = {
    'name': 'commanderbot-lib',
    'version': '0.1.0',
    'description': 'A library of utilities for discord.py bots.',
    'long_description': '# CommanderBot Lib\n\nA library of utilities for discord.py bots.\n',
    'author': 'Arcensoth',
    'author_email': 'arcensoth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CommanderBot-Dev/commanderbot-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
