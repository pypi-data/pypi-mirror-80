# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crystal_toolkit',
 'crystal_toolkit.apps',
 'crystal_toolkit.apps.examples',
 'crystal_toolkit.apps.examples.tests',
 'crystal_toolkit.apps.tests',
 'crystal_toolkit.components',
 'crystal_toolkit.components.transformations',
 'crystal_toolkit.core',
 'crystal_toolkit.core.tests',
 'crystal_toolkit.helpers',
 'crystal_toolkit.renderables']

package_data = \
{'': ['*'], 'crystal_toolkit.apps': ['assets/*']}

install_requires = \
['ifermi>=0.1.2,<0.2.0',
 'plotly>=4.5.4,<5.0.0',
 'pydantic>=1.4,<2.0',
 'pyfftw>=0.12.0,<0.13.0',
 'pymatgen>=2020.9.14,<2021.0.0',
 'webcolors>=1.11.1,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing-extensions>=3.7,<4.0'],
 'server': ['dash>=1.16,<2.0',
            'dash-daq>=0.4.0,<0.5.0',
            'gunicorn>=20.0.4,<21.0.0',
            'redis>=3.4.1,<4.0.0',
            'Flask-Caching>=1.8.0,<2.0.0',
            'gevent>=1.4.0,<2.0.0',
            'dash-mp-components>=0.0.25',
            'scikit-learn>=0.22.2,<0.23.0',
            'robocrys>=0.2.1,<0.3.0',
            'scikit-image>=0.17.2,<0.18.0',
            'habanero>=0.7.2,<0.8.0',
            'hiphive>=0.7,<0.8',
            'dscribe>=0.3.5,<0.4.0',
            'dash-extensions>=0.0.31,<0.0.32',
            'sentry-sdk>=0.17.3,<0.18.0']}

setup_kwargs = {
    'name': 'crystal-toolkit',
    'version': '2020.9.28',
    'description': '',
    'long_description': None,
    'author': 'Matthew Horton',
    'author_email': 'mkhorton@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
