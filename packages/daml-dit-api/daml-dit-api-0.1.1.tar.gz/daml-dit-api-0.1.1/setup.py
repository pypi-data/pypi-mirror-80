# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daml_dit_api', 'daml_dit_api.main']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp', 'dacite', 'dazl>=7,<8']

setup_kwargs = {
    'name': 'daml-dit-api',
    'version': '0.1.1',
    'description': 'DABL Integrations API Package',
    'long_description': 'daml-dit-api\n====\n\nAPI definitions for integrations to be hosted by DABL. This contains\nthe basic data types and function call definition, as well as as a\nframework for simplifing the implementation of integrations.\n',
    'author': 'Mike Schaeffer',
    'author_email': 'mike.schaeffer@digitalasset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digital-asset/daml-dit-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
