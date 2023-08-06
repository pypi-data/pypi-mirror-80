# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turbulette',
 'turbulette.alembic',
 'turbulette.apps',
 'turbulette.apps.auth',
 'turbulette.apps.auth.policy',
 'turbulette.apps.auth.resolvers',
 'turbulette.apps.auth.resolvers.queries',
 'turbulette.apps.base',
 'turbulette.apps.base.resolvers',
 'turbulette.asgi',
 'turbulette.conf',
 'turbulette.core',
 'turbulette.core.management',
 'turbulette.core.management.templates.app',
 'turbulette.core.management.templates.project',
 'turbulette.core.management.templates.project.alembic',
 'turbulette.core.validation',
 'turbulette.db',
 'turbulette.middleware',
 'turbulette.test',
 'turbulette.type',
 'turbulette.utils']

package_data = \
{'': ['*'],
 'turbulette.apps.auth': ['graphql/queries/*', 'graphql/types/*'],
 'turbulette.apps.base': ['graphql/*'],
 'turbulette.core.management.templates.app': ['graphql/*', 'resolvers/*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'ariadne>=0.11,<0.13',
 'async-caches>=0.3.0,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'gino[starlette]>=1.0.1,<2.0.0',
 'passlib[bcrypt]>=1.7.2,<2.0.0',
 'psycopg2>=2.8.5,<3.0.0',
 'pydantic[email]>=1.6.1,<2.0.0',
 'python-jwt>=3.2.6,<4.0.0',
 'simple-settings>=0.19.1,<0.20.0']

entry_points = \
{'console_scripts': ['turb = turbulette.core.management.cli:cli'],
 'pytest11': ['turbulette = turbulette.test.pytest_plugin']}

setup_kwargs = {
    'name': 'turbulette',
    'version': '0.2.0',
    'description': 'A Framework to build async GraphQL APIs with Ariadne and GINO',
    'long_description': '# Turbulette\n\n![test](https://github.com/python-turbulette/turbulette/workflows/test/badge.svg)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/e244bb031e044079af419dabd40bb7fc)](https://www.codacy.com/gh/python-turbulette/turbulette/dashboard?utm_source=github.com&utm_medium=referral&utm_content=python-turbulette/turbulette&utm_campaign=Badge_Coverage)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e244bb031e044079af419dabd40bb7fc)](https://www.codacy.com/gh/python-turbulette/turbulette/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=python-turbulette/turbulette&amp;utm_campaign=Badge_Grade)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Generic badge](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![Generic badge](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nWIP\n',
    'author': 'Matthieu MN',
    'author_email': 'matthieu.macnab@pm.me',
    'maintainer': 'Matthieu MN',
    'maintainer_email': 'matthieu.macnab@pm.me',
    'url': 'https://github.com/gazorby/turbulette',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
