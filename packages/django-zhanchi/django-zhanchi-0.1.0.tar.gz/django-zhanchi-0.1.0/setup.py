# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_zhanchi']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'django-zhanchi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Furkan Karataş',
    'author_email': 'furkan.karatas02@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
