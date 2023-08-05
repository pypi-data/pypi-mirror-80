# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcwiki']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'mcwiki',
    'version': '0.0.0',
    'description': 'A scraping library for the Minecraft wiki',
    'long_description': '# mcwiki\n\n> A scraping library for the Minecraft wiki.\n\n```python\nimport mcwiki\n\npage = mcwiki.load("Advancement/JSON format")\nsection = page["File Format"]\nprint(section.extract(mcwiki.TREE))\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/mcwiki/blob/master/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/mcwiki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
