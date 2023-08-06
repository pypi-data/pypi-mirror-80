# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgtg']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.24.0']

setup_kwargs = {
    'name': 'tgtg',
    'version': '0.2.0',
    'description': 'Unoffical python client for TooGoodToGo API',
    'long_description': '[![Actions Status](https://github.com/ahivert/tgtg-python/workflows/CI/badge.svg)](https://github.com/ahivert/tgtg-python/actions)\n[![codecov](https://codecov.io/gh/ahivert/tgtg-python/branch/master/graph/badge.svg)](https://codecov.io/gh/ahivert/tgtg-python)\n[![PyPI version](https://img.shields.io/pypi/v/tgtg?color=blue)](https://pypi.org/project/tgtg/)\n\n# tgtg-python\n\nPython client that help you to talk with [TooGoodToGo](https://toogoodtogo.com) API.\n\nPython version: 3.6, 3.7, 3.8\n\nHandle:\n- login (`/api/auth/v1/loginByEmail`)\n- list stores (`/api/item/`)\n- get a store (`/api/item/:id`)\n- get all stores (`/api/map/v1/listAllBusinessMap`)\n- set favorite (`/api/item/:id/setFavorite`)\n\nUsed by:\n- https://tgtg-notifier.com\n\n## Install\n\n```\npip install tgtg\n```\n\n## Use it\n\n```python\nfrom tgtg import TgtgClient\n\n# login with email and password\nclient = TgtgClient(email=your_email, password=your_password)\n\n# or you can login with user_id and access_token\n# (you can retrieve them from client after logged with email and password)\nclient = TgtgClient(access_token=your_access_token, user_id=your_user_id)\n\n# You can then get some items, default will get **only** your favorites\nclient.get_items()\n\n# To get items (not only your favorites) you need to provide location informations\nclient.get_items(\n    favorites_only=False,\n    latitude=48.126,\n    longitude=-1.723,\n    radius=10,\n)\n\n# Or get an item\nclient.get_item(1234)\n\n```\n\n## Developers\n\nThis project uses poetry so you will need to install poetry locally to use following\ncommands.\n```\npip install poetry --user\npoetry install\n```\n\nThis project uses [black](https://github.com/psf/black) to format all the code,\n[isort](https://github.com/timothycrosley/isort) to sort all imports and\nlint is done by [flake8](https://github.com/PyCQA/flake8).\n\nJust run this command to format automatically all the code you wrote:\n```\nmake style\n```\n\nRun this command to run all tests:\n```\nmake test\n```\n',
    'author': 'Anthony Hivert',
    'author_email': 'anthony.hivert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ahivert/tgtg-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
