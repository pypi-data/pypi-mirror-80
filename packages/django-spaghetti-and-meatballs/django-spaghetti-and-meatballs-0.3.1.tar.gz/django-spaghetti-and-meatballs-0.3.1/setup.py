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
    'version': '0.3.1',
    'description': 'Its a spicy meatball for serving up fresh hot entity-relationship diagrams straight from your django models.',
    'long_description': 'django-spaghetti-and-meatballs\n==============================\n\n|docs| |travis| |code-climate| |coveralls|\n\nIts a spicy meatball for serving up fresh hot entity-relationship diagrams straight from your django models.\n\n\nAdding spaghetti to your project\n--------------------------------\n\nInstall some spaghetti:\n\n.. code-block:: sh\n\n  pip install django-spaghetti-and-meatballs\n\nAdd ``"django_spaghetti"`` to your ``INSTALLED_APPS`` setting like this:\n\n.. code-block:: python\n\n  INSTALLED_APPS = [\n      ...\n      \'django_spaghetti\',\n  ]\n\nConfigure your sauce\n++++++++++++++++++++\n\n``django-spaghetti-and-meatballs`` takes a few options set in the ``SPAGHETTI_SAUCE``\nvariable from your projects ``settings.py`` file that make it `extra spicy`:\n\n.. code-block:: python\n\n  SPAGHETTI_SAUCE = {\n      \'apps\': [\'auth\', \'polls\'],\n      \'show_fields\': False,\n      \'exclude\': {\'auth\': [\'user\']},\n  }\n\nIn the above dictionary, the following settings are used:\n\n* ``apps`` is a list of apps you want to show in the graph. If its `not` in here it `won\'t be seen`.\n* ``show_fields`` is a boolean that states if the field names should be shown in the graph or just in the however over. For small graphs, you can set this to `True` to show fields as well, but as you get more models it gets messier.\n* ``exclude`` is a dictionary where each key is an ``app_label`` and the items for that key are model names to hide in the graph. \n\nIf its not working as expected make sure your app labels and model names are all **lower case**.\n\n\nServe your plate in your urls file\n++++++++++++++++++++++++++++++++++\n\nOnce you\'ve configured your sauce, make sure you serve up a plate of spaghetti in your ``urls.py`` like so:\n\n.. code-block:: python\n\n    urlpatterns += patterns(\'\',\n        url(r\'^plate/\', include(\'django_spaghetti.urls\')),\n    )\n\nA sample platter\n----------------\n\nBelow is an example image showing the connections between models from the \n`django-reversion <https://github.com/etianen/django-reversion>`_ and \n`django-notifications <https://github.com/django-notifications/django-notifications>`_ \napps and Django\'s built-in ``auth`` models.\n\nColored edges illustrate foreign key relations, with arrows pointing from the defining \nmodel to the related model, while gray edges illustrate many-to-many relations. \nDifferent colors signify the different Django apps, and when relations link between \napps the edges are colored with a gradient.\n\n.. image:: https://cloud.githubusercontent.com/assets/2173174/9053053/a45e185c-3ab2-11e5-9ea0-89dafb7ac274.png\n\nHovering over a model, gives a pop-up that lists the following information:\n\n* model name\n* app label\n* The models docstring\n* A list of every field, with its field type and its help text (if defined). Unique fields have their name underlined.\n\nThis was build with the sauce:\n\n.. code-block:: python\n\n  SPAGHETTI_SAUCE = {\n      \'apps\': [\'auth\', \'notifications\', \'reversion\'],\n      \'show_fields\': False,\n  }\n\nA complex live-demo\n-------------------\n\nTo see a complex example, where ``django-spaghetti-and-meatballs`` really shines,\ncheckout the live version built for the `Aristotle Metadata Registry <http://registry.aristotlemetadata.com/labs/plate/>`_\n\n.. |docs| image:: https://readthedocs.org/projects/django-spaghetti-and-meatballs/badge/?version=latest\n    :target: https://django-spaghetti-and-meatballs.readthedocs.io/en/latest/\n    :alt: Documentation Status\n\n.. |code-climate| image:: https://codeclimate.com/github/LegoStormtroopr/django-spaghetti-and-meatballs/badges/gpa.svg\n   :target: https://codeclimate.com/github/LegoStormtroopr/django-spaghetti-and-meatballs\n   :alt: Code Climate\n\n.. |coveralls| image:: https://coveralls.io/repos/LegoStormtroopr/django-spaghetti-and-meatballs/badge.svg?branch=master&service=github\n   :target: https://coveralls.io/github/LegoStormtroopr/django-spaghetti-and-meatballs?branch=master\n\n.. |travis| image:: https://travis-ci.org/LegoStormtroopr/django-spaghetti-and-meatballs.svg?branch=master\n    :target: https://travis-ci.org/LegoStormtroopr/django-spaghetti-and-meatballs\n',
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
