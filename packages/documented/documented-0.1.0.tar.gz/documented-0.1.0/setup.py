# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['documented']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'documented',
    'version': '0.1.0',
    'description': 'Human readable Python exceptions.',
    'long_description': '# documented\n\n[![Build Status](https://travis-ci.com/python-platonic/documented.svg?branch=master)](https://travis-ci.com/python-platonic/documented)\n[![Coverage](https://coveralls.io/repos/github/python-platonic/documented/badge.svg?branch=master)](https://coveralls.io/github/python-platonic/documented?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/documented.svg)](https://pypi.org/project/documented/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nTemplated docstrings for Python classes.\n\n## Features\n\n- Describe your business logic in docstrings of your classes and exceptions;\n- When printing an object or an exception, your code will explain to you what is going on.\n\n## Installation\n\n```bash\npip install documented\n```\n\n\n## Example\n\n```python\nfrom dataclasses import dataclass\nfrom documented import DocumentedError\n\n\n@dataclass\nclass InsufficientWizardryLevel(DocumentedError):\n    """\n    🧙 Your level of wizardry is insufficient ☹\n\n        Spell: {self.spell}\n        Minimum level required: {self.required_level}\n        Actual level: {self.actual_level} {self.comment}\n\n    Unseen University will be happy to assist in your training! 🎓\n    """\n\n    spell: str\n    required_level: int\n    actual_level: int\n\n    @property\n    def comment(self) -> str:\n        if self.actual_level <= 0:\n            return \'(You are Rincewind, right? Hi!)\'\n        else:\n            return \'\'\n\n\nraise InsufficientWizardryLevel(\n    spell=\'Animal transformation\',\n    required_level=8,\n    actual_level=0,\n)\n```\n\nwhich prints:\n\n```\n---------------------------------------------------------------------\nInsufficientWizardryLevel           Traceback (most recent call last)\n<ipython-input-1-d8ccdb953cf6> in <module>\n     27 \n     28 \n---> 29 raise InsufficientWizardryLevel(\n     30     spell=\'Animal transformation\',\n     31     required_level=8,\n\nInsufficientWizardryLevel: \n🧙 Your level of wizardry is insufficient ☹\n\n    Spell: Animal transformation\n    Minimum level required: 8\n    Actual level: 0 (You are Rincewind, right? Hi!)\n\nUnseen University will be happy to assist in your training! 🎓\n```\n\n## License\n\n[MIT](https://github.com/python-platonic/documented/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [5840464a31423422d7523897d854e92408eee6b8](https://github.com/wemake-services/wemake-python-package/tree/5840464a31423422d7523897d854e92408eee6b8). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/5840464a31423422d7523897d854e92408eee6b8...master) since then.\n',
    'author': 'Anatoly Scherbakov',
    'author_email': 'altaisoft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-platonic/documented',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
