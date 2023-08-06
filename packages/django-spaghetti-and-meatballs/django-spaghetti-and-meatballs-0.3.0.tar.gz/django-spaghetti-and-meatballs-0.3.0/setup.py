# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_spaghetti', 'django_spaghetti.tests']

package_data = \
{'': ['*'],
 'django_spaghetti': ['locale/en/LC_MESSAGES/*',
                      'locale/fr/LC_MESSAGES/*',
                      'templates/django_spaghetti/*'],
 'django_spaghetti.tests': ['templates/tests/*']}

install_requires = \
['django>=2.2']

setup_kwargs = {
    'name': 'django-spaghetti-and-meatballs',
    'version': '0.3.0',
    'description': 'Its a spicy meatball for serving up fresh hot entity-relationship diagrams straight from your django models.',
    'long_description': None,
    'author': 'Samuel Spencer',
    'author_email': 'sam@sqbl.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
