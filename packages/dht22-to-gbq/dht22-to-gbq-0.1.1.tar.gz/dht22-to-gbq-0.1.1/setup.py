# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dht_to_gbq']

package_data = \
{'': ['*']}

install_requires = \
['adafruit-dht-fixed>=1.4.2,<2.0.0', 'google-cloud-bigquery>=1.28.0,<2.0.0']

entry_points = \
{'console_scripts': ['dht_to_gbq = dht_to_gbq.__init__:main']}

setup_kwargs = {
    'name': 'dht22-to-gbq',
    'version': '0.1.1',
    'description': 'Requests data from a DHT22 sensor and inserts it into Google BigQuery.',
    'long_description': None,
    'author': 'Jan-Benedikt Jagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
