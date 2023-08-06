# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosql', 'aiosql.adapters']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'aiosql',
    'version': '3.1.3',
    'description': 'Simple SQL in Python.',
    'long_description': '# aiosql\n\nSimple SQL in Python\n\nSQL is code, you should be able to write it, version control it, comment it, and run it using files. Writing your SQL code in Python programs as strings doesn\'t allow you to easily reuse your SQL in database GUI tools or CLI tools like psql. With aiosql you can organize your SQL statements in _.sql_ files, load them into your python application as methods to call without losing the ability to use them as you would any other SQL file.\n\nThis project supports standard and [asyncio](https://docs.python.org/3/library/asyncio.html) based drivers for SQLite and PostgreSQL out of the box ([sqlite3](https://docs.python.org/3/library/sqlite3.html), [aiosqlite](https://aiosqlite.omnilib.dev/en/latest/?badge=latest), [psycopg2](https://www.psycopg.org/docs/), [asyncpg](https://magicstack.github.io/asyncpg/current/)). Extensions to support other database drivers can be written by you!\n\nIf you are using python versions <3.6 please see the related [anosql](https://github.com/honza/anosql) package which this project is based on.\n\n## Documentation\n\nProject and API docs https://nackjicholson.github.io/aiosql\n\n## Install\n\n```\npip install aiosql\n```\n\nOr if you you use [poetry](https://python-poetry.org):\n\n```\npoetry add aiosql\n```\n\n## Usage\n\nGiven you have a SQL file like the one below called `users.sql`\n\n```sql\n-- name: get-all-users\n-- Get all user records\nselect userid,\n       username,\n       firstname,\n       lastname\n  from users;\n\n\n-- name: get-user-by-username^\n-- Get user with the given username field.\nselect userid,\n       username,\n       firstname,\n       lastname\n  from users\n where username = :username;\n```\n\nYou can use `aiosql` to load the queries in this file for use in your Python application:\n\n```python\nimport aiosql\nimport sqlite3\n\nconn = sqlite3.connect("myapp.db")\nqueries = aiosql.from_path("users.sql", "sqlite3")\n\nusers = queries.get_all_users(conn)\n# >>> [(1, "nackjicholson", "William", "Vaughn"), (2, "johndoe", "John", "Doe"), ...]\n\nusers = queries.get_user_by_username(conn, username="nackjicholson")\n# >>> (1, "nackjicholson", "William", "Vaughn")\n```\n\nWriting SQL in a file and executing it from methods in python!\n\n## Why you might want to use this\n\n- You think SQL is pretty good, and writing SQL is an important part of your applications.\n- You don\'t want to write your SQL in strings intermixed with your python code.\n- You\'re not using an ORM like SQLAlchemy or Django, and you don\'t need to.\n- You want to be able to reuse your SQL in other contexts. Loading it into psql or other database tools.\n\n## Why you might _NOT_ want to use this\n\n- You\'re looking for an ORM.\n- You aren\'t comfortable writing SQL code.\n- You don\'t have anything in your application that requires complicated SQL beyond basic CRUD operations.\n- Dynamically loaded objects built at runtime really bother you.\n',
    'author': 'William Vaughn',
    'author_email': 'vaughnwilld@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nackjicholson/aiosql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
