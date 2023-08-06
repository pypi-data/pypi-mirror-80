# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marshmallow_geojson']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.8.0,<4.0.0', 'ujson>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'marshmallow-geojson',
    'version': '0.1.4',
    'description': 'Marshmallow schema validation for GeoJson',
    'long_description': '\n.. image:: https://travis-ci.org/folt/marshmallow-geojson.svg\n   :target: https://travis-ci.org/github/folt/marshmallow-geojson\n   :alt: Travis\n\n.. image:: https://codecov.io/gh/folt/marshmallow-geojson/branch/master/graph/badge.svg?token=B5ATYXLBHO\n   :target: https://codecov.io/gh/folt/marshmallow-geojson\n   :alt: Codecov\n\nmarshmallow_geojson\n===================\n\n',
    'author': 'Aliaksandr Vaskevich',
    'author_email': 'vaskevic.an@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/folt/marshmallow-geojson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
