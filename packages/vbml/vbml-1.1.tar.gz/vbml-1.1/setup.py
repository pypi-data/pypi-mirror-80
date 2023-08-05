# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vbml',
 'vbml.patcher',
 'vbml.pattern',
 'vbml.pattern.validation',
 'vbml.utils',
 'vbml.validator']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'vbml',
    'version': '1.1',
    'description': 'Way to check, match & resist. Sofisticated object oriented regex-based text parser',
    'long_description': '<p align="center">\n  <a href="https://github.com/tesseradecade/vbml">\n    <img src="/logo.jpeg" width="200px" style="display: inline-block;">\n  </a>\n</p>\n<h1 align="center">\n  [VBML] perfect pythonistic parser / string manipulator :sparkles:\n</h1>\n<p align="center">\n  <img alt="PyPI - License" src="https://img.shields.io/pypi/l/vbml?style=flat-square">\n  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/vbml?style=flat-square">\n  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/tesseradecade/vbml?style=flat-square">\n  <img alt="GitHub issues by-label" src="https://img.shields.io/github/issues/tesseradecade/vbml/bug?style=flat-square">\n</p>\n\n## Features\n\n* Clean `regex`-based parser\n* Easy-to-understand validators / Custom validators\n* Lots of features out-of-box\n\n`I am <name>, i am <age:int> years old` + `I am Steven, i am 20 years old` = `{"name": "Steven", "age": 20}`\n\n## Installation\n\nInstall with pip:\n\n```shell script\npip install vbml\n```\n\nOr with poetry:\n\n```shell script\npoetry add vbml\n```\n\n## Run tests\n\nClone repo from git:\n\n```shell script\ngit clone https://github.com/tesseradecade/vbml.git\n```\n\nGo to repository and run tests with `poetry`:\n\n```shell script\ncd vbml\npoetry install\npoetry run pytest\n```\n\n## :book: Documentation\n\nFull documentation contents are available in [docs/index.md](/docs/index.md)\n\n## Simple example\n\n```python\nfrom vbml import Patcher, Pattern\n\npatcher = Patcher()\npattern = Pattern("He is <description> like he has right just turned <age:int> years old")\n\nresult1 = patcher.check(pattern, "He is so spontaneous like he has right just turned 10 years old")\nresult2 = patcher.check(pattern, "He is silly like he has right just turned t3n years old")\nresult3 = patcher.check(pattern, "Haha regex go brrr")\n\nresult1 # {"description": "so spontaneous", "age": 10}\nresult2 # None\nresult3 # None\n```\n\nLeave a :star: if this project helped you  \nMade with :heart: by [timoniq](https://github.com/timoniq)\n',
    'author': 'timoniq',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tesseradecade/vbml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
