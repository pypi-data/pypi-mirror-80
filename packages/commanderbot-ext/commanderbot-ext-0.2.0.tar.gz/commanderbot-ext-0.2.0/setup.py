# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commanderbot_ext', 'commanderbot_ext.faq', 'commanderbot_ext.status']

package_data = \
{'': ['*']}

install_requires = \
['commanderbot-lib>=0.1.0,<0.2.0', 'discord.py>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'commanderbot-ext',
    'version': '0.2.0',
    'description': 'A collection of cogs and extensions for discord.py bots.',
    'long_description': '# CommanderBot Ext\n\nA collection of cogs and extensions for discord.py bots.\n',
    'author': 'Arcensoth',
    'author_email': 'arcensoth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CommanderBot-Dev/commanderbot-ext',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
