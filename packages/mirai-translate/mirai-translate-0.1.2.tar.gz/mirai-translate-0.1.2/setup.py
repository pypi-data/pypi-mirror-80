# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirai_translate']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'httpx>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'mirai-translate',
    'version': '0.1.2',
    'description': 'Unofficial Mirai Translate API for Python',
    'long_description': "# mirai-translate\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mirai-translate)\n![PyPI](https://img.shields.io/pypi/v/mirai-translate)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/reiyw/mirai-translate/Tests)\n\nmirai-translate is an unofficial [Mirai Translate](https://miraitranslate.com/en/) API for Python.\n\n```\npip install mirai-translate\n```\n\n```python\n>>> from mirai_translate import Client\n>>> cli = Client()\n>>> cli.translate('テスト', 'ja', 'en')\n'Test'\n```\n\n## Disclaimer\n\nmirai-translate simply accesses [Translation Demo](https://miraitranslate.com/en/trial/) and requests to the behind API server.\nI believe there is no illegality in using this library.\nHowever, you might want to read the [Terms of Use for Mirai Translate](https://miraitranslate.com/en/trial/pdf/kiyaku.pdf).\n",
    'author': 'reiyw',
    'author_email': 'reiyw.setuve@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reiyw/mirai-translate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
