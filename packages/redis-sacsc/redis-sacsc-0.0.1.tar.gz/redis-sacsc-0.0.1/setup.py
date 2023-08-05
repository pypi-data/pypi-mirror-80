# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_sacsc']

package_data = \
{'': ['*']}

install_requires = \
['redis>=3.4.1,<4.0.0']

setup_kwargs = {
    'name': 'redis-sacsc',
    'version': '0.0.1',
    'description': 'Redis Server-Assisted Client-Side Caching in Python',
    'long_description': '[![Build Status](https://travis-ci.com/iamajay/redis-sacsc.svg?branch=master)](https://travis-ci.com/iamajay/redis-sacsc)\n[![Coverage](https://coveralls.io/repos/github/iamajay/redis-sacsc/badge.svg?branch=master)](https://coveralls.io/github/iamajay/redis-sacsc?branch=master)\n\n# redis-sacsc\n\nRedis Server-Assisted Client-Side Caching in Python\n\n#### WARNING!\nThis feature is still in redis beta release, scheduled to be released in version 6\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Redis Server-Assisted Client-Side Caching\n\n\n## Installation\n\n```bash\npip install redis-sacsc\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nimport redis\nfrom redis_sacsc import Manager\npool = redis.ConnectionPool.from_url("redis://127.0.0.1:6379")\nmanager = Manager(pool, capacity=512)\nredis_conn = manager.get_connection()\nredis_conn.set(\'foo\', \'bar\')\nredis_conn.get(\'foo\')\n# => \'bar\'\n\n```\n\n## License\n\n[MIT](https://github.com/iamajay/redis-sacsc/blob/master/LICENSE)\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iamajay/redis-sacsc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
