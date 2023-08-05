# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_beautysh']

package_data = \
{'': ['*']}

install_requires = \
['beautysh>=6.0.0', 'mdformat>=0.1.2']

entry_points = \
{'mdformat.codeformatter': ['bash = mdformat_beautysh:format_bash',
                            'sh = mdformat_beautysh:format_bash']}

setup_kwargs = {
    'name': 'mdformat-beautysh',
    'version': '0.1.0',
    'description': 'Mdformat plugin to beautify Bash scripts',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-beautysh/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-beautysh/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)\n[![PyPI version](https://badge.fury.io/py/mdformat-beautysh.svg)](<https://badge.fury.io/py/mdformat-beautysh>)\n\n# mdformat-beautysh\n> Mdformat plugin to beautify Bash scripts\n\n## Description\nmdformat-beautysh is an [mdformat](https://github.com/executablebooks/mdformat) plugin\nthat makes mdformat format Bash scripts with [Beautysh](https://github.com/lovesegfault/beautysh).\n## Usage\nInstall with:\n```console\npip install mdformat-beautysh\n```\n\nWhen using mdformat on the command line, Beautysh formatting will be automatically enabled after install.\n\nWhen using mdformat Python API, code formatting for Bash scripts will have to be enabled explicitly:\n```python\nimport mdformat\n\n\nunformatted = """~~~bash\nfunction bad_func()\n {\necho "test"\n}\n~~~\n"""\n\nformatted = mdformat.text(unformatted, codeformatters={"bash", "sh"})\n\nassert formatted == """~~~bash\nfunction bad_func()\n{\n    echo "test"\n}\n~~~\n"""\n```\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-beautysh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
