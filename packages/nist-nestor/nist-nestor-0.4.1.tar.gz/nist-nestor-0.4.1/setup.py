# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nestor', 'nestor.datasets']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0',
 'networkx>=2.4,<3.0',
 'pyyaml>=5.3.1,<6.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'seaborn>=0.10.1,<0.11.0',
 'tables>=3.6.1,<4.0.0',
 'tqdm>=4.48.2,<5.0.0']

setup_kwargs = {
    'name': 'nist-nestor',
    'version': '0.4.1',
    'description': 'Quantifying tacit human knowledge for Smart Manufacturing Maintenance, for maintnenance-based investigatory analysis',
    'long_description': None,
    'author': 'tbsexton',
    'author_email': 'thurston.sexton@nist.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.nist.gov/services-resources/software/nestor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
