# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guillotina_graphql', 'guillotina_graphql.tests']

package_data = \
{'': ['*']}

install_requires = \
['ariadne>=0.12.0,<0.13.0', 'guillotina>=6.0.8,<7.0.0']

setup_kwargs = {
    'name': 'guillotina-graphql',
    'version': '0.1.0',
    'description': '',
    'long_description': "# guillotina_graphql\n\n## Dependencies\n\nPython >= 3.7\n\nGuillotina >= 6.0.0\n\n\n## Installation\n\n> **Warning:** you need to use a postgres database and have enabled `guillotina.contrib.catalog.pg`\n\n0. Install the plugin:\n\n```bash\npip install guillotina_graphql\n```\n\n1. Add `guillotina_graphql` to your settings\n\n```yaml\napplications:\n - your_app\n - guillotina_graphql\n - guillotina.contrib.catalog.pg\n```\n\nand optionally:\n```yaml\ngraphql:\n  enable_playground: true\n```\n\n2. You're ready!\n\n\n## Start using GraphQL\n\nThis is the route to the GraphQL endpoint: `http://localhost:8080/<your-db>/<your-container>/@graphql` (needs authentification with permission AccessContent).\n\nYou can use the playground on a browser http://localhost:8080/@graphql-playground\n",
    'author': 'Jordi Masip',
    'author_email': 'jordi@masip.cat',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
