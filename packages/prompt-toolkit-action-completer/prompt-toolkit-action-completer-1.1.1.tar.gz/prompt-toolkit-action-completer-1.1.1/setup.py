# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['action_completer']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0',
 'fuzzywuzzy[speedup]>=0.18.0,<0.19.0',
 'prompt-toolkit>=3.0.7,<4.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'prompt-toolkit-action-completer',
    'version': '1.1.1',
    'description': 'A fairly simple method for registering callables as prompt-toolkit completions',
    'long_description': '# Action Completer\n\n[![Supported Versions](https://img.shields.io/pypi/pyversions/prompt-toolkit-action-completer.svg)](https://pypi.org/project/prompt-toolkit-action-completer/)\n[![Test Status](https://github.com/stephen-bunn/prompt-toolkit-action-completer/workflows/Test%20Package/badge.svg)](https://github.com/stephen-bunn/prompt-toolkit-action-completer/actions?query=workflow%3A%22Test+Package%22)\n[![codecov](https://codecov.io/gh/stephen-bunn/prompt-toolkit-action-completer/branch/master/graph/badge.svg)](https://codecov.io/gh/stephen-bunn/prompt-toolkit-action-completer)\n[![Documentation Status](https://readthedocs.org/projects/prompt-toolkit-action-completer/badge/?version=latest)](https://prompt-toolkit-action-completer.readthedocs.org/)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)\n\n**A fairly simple method for registering callables as prompt-toolkit completions.**\n\nThis package provides the basic features to easily construct a custom completer using\ndecorators to reduce the amount of boilerplate needed to build basic tooling through\n[prompt-toolkit](http://python-prompt-toolkit.readthedocs.io/en/stable).\nA quick example is provided below, but if you are interested in the available features\nand patterns you should read through [the documentation](https://prompt-toolkit-action-completer.readthedocs.org/).\n\nThis is a project that I originally created for myself several times when building\npersonal utilities with prompt-toolkit, and figured it might be useful for other people\nto eventually use or extend.\nAs a side-effect of this being a personal utility, the provided functionality may not\n*exactly* fit what you are looking for and the provided tests do not check all edge\ncases properly yet.\n\n```python\nfrom pathlib import Path\n\nfrom action_completer import ActionCompleter\nfrom prompt_toolkit.shortcuts import prompt\nfrom prompt_toolkit.completion import PathCompleter\nfrom prompt_toolkit.validation import Validator\n\ncompleter = ActionCompleter()\n\n\n@completer.action("cat")\n@completer.param(\n  PathCompleter(),\n  cast=Path,\n  validators=[\n      Validator.from_callable(\n        lambda p: Path(p).is_file(),\n        error_message="Path is not an existing file"\n      )\n  ]\n)\ndef _cat_action(filepath: Path):\n  with filepath.open("r") as file_handle:\n      print(file_handle.read())\n\n\nprompt_result = prompt(\n  ">>> ",\n  completer=completer,\n  validator=completer.get_validator()\n)\ncompleter.run_action(prompt_result)\n```\n\n![Example Recording](docs/source/_static/assets/recordings/004-cat-path-validation.gif)\n',
    'author': 'Stephen Bunn',
    'author_email': 'stephen@bunn.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephen-bunn/prompt-toolkit-action-completer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
