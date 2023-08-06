# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['downloads']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'downloads',
    'version': '1.0.0',
    'description': 'Easy file downloads',
    'long_description': '# Downloads\n\n[![test](https://github.com/audy/downloads/workflows/test/badge.svg)](https://github.com/audy/downloads/actions?query=workflow%3Atest)\n[![PyPI version](https://badge.fury.io/py/downloads.svg)](https://badge.fury.io/py/downloads)\n[![Downloads](https://pepy.tech/badge/downloads/month)](https://pepy.tech/project/downloads)\n\nEasier HTTP downloads in Python 3.5+\n\n## Features\n\n1. Easier to remember than `urllib`\n2. Files are not written unless download finishes\n3. Progress bar!\n\n## Installation\n\n```\npip install downloads==1.0.0\n```\n\n## Usage\n\n```python\nfrom downloads import download\n\ndownload("http://i.imgur.com/ij2h06p.png")\n\n# output path is automatically determined and returned\n# but you can specify it manually if that"s your thing:\n\ndownload("http://i.imgur.com/i5pJRxX.jpg", out_path="cheezburger.jpg")\n\n# or, if you want to be fancy:\n\ndownload("https://www.gutenberg.org/files/2600/2600-0.txt", progress=True)\n```\n\nThat\'s it!\n\n',
    'author': 'Austin Davis-Richardson',
    'author_email': 'harekrishna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
