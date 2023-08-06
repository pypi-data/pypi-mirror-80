# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ogadf_schema']

package_data = \
{'': ['*']}

install_requires = \
['fits-schema>=0.5.4,<0.6.0']

setup_kwargs = {
    'name': 'ogadf-schema',
    'version': '0.2.3',
    'description': 'Schema definitions for the Data Formats For Gamma-Ray Astronomy',
    'long_description': '# ogadf-schema\nDefinition of the open gamma ray astronomy data formats using fits-schema\n',
    'author': 'Maximilian Nöthe',
    'author_email': 'maximilian.noethe@tu-dortmund.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
