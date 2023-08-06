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
    'version': '0.1.0',
    'description': 'Marshmallow schema validation for GeoJson',
    'long_description': None,
    'author': 'Aliaksandr Vaskevich',
    'author_email': 'vaskevic.an@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
