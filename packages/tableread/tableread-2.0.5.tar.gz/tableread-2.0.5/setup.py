# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tableread']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=16.0.0']

setup_kwargs = {
    'name': 'tableread',
    'version': '2.0.5',
    'description': 'Table reader for simple reStructuredText tables',
    'long_description': 'TableRead\n=========\n\nTableRead is a script designed to read reStructredText (reST) `simple tables`_ from a file and convert them into Python objects.\n\n\nQuickstart\n----------\n\nSay you have a simple table like this located in a ``./example.rst``::\n\n    ++++++++++++\n    Damage Doers\n    ++++++++++++\n\n    ======  ===  ==============\n    Name    Age  Favorite Color\n    ======  ===  ==============\n    Mookie  26   Red\n    Andrew  24   Red\n    JD      31   Red\n    Xander  26   Red\n    ======  ===  ==============\n\nHere are a few useful things you can do with that table::\n\n    >>> from tableread import SimpleRSTReader\n    >>>\n    >>> reader = SimpleRSTReader("./example.rst")\n    >>> reader.tables\n    [\'Damage Doers\']\n    >>>\n    >>> table = reader["Damage Doers"]\n    >>> table.fields\n    [\'name\', \'age\', \'favorite_color\']\n    >>>\n    >>> for row in table:\n    ...     print(row.favorite_color)\n    ...\n    Red\n    Red\n    Red\n    Red\n    >>>\n    >>> for row in table.matches_all(age="26"):\n    ...     print(row.name)\n    ...\n    Mookie\n    Xander\n    >>>\n    >>> for row in table.exclude_by(age="26"):\n    ...     print(row.name)\n    ...\n    Andrew\n    JD\n\nUsage\n-----\n\n``class tableread.SimpleRSTReader(file_path)``\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n    Parse a reStructredText file, ``file_path``, and convert any simple tables into ``SimpleRSTTable`` objects.\n    Individual tables can be accessed using the table name as the key (``SimpleRSTReader[\'table_name\']``)\n\n**data**\n  An OrderedDict of the table(s) found in the reST file. The key is either the\n  section header before the table name from the file, or ``Default`` for tables not under a header.\n  For multiple tables in a section (or multiple ``Default`` tables),\n  subsequent tables will have a incrementing number appended to the key: ``Default``, ``Default_2``, etc.\n  The value is a ``SimpleRSTTable`` object.\n\n**tables**\n  A list of the table names; an alias for ``list(data.keys())``\n\n**first**\n  A helper to get the first table found in the file; an alias for\n  ``list(self.data.values())[0]``\n\n\n``class tableread.SimpleRSTTable(header, rows, column_spans)``\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n    A representation of an individual table. In addition to the methods below,\n    you may iterate over the table itself as a shortcut (``for entry in table:``),\n    which will yield from ``table.data``.\n    ``len(table)`` will also return the number of entries in ``table.data``.\n\n**data**\n  A list of namedtuples with ``fields`` as the names.\n\n**fields**\n  A tuple of the table fields, as used in the ``data`` namedtuple.\n  Field names are adapted from table columns by lower-casing,\n  and replacing spaces and periods with underscores.\n\n**from_data(data)**\n  A helper function to create an object with. Expects a prepared list of namedtuples.\n\n**matches_all(**kwargs)**\n  Given a set of key/value filters, returns a new TableRead object with only\n  the filtered data, that can be iterated over.\n  Values may be either a simple value (str, int) or a function that returns a boolean.\n  See Quickstart_ for an example.\n\n  Note: When filtering both keys and values are **not** case sensitive.\n\n**exclude_by(**kwargs)**\n  Given a set of key/value filters, returns a new TableRead object without the\n  matching data, that can be iterated over.\n  Values may be either a simple value (str, int) or a function that returns a boolean.\n  See Quickstart_ for an example.\n\n  Note: When filtering both keys and values are **not** case sensitive.\n\n**get_fields(*fields)**\n  Given a list of fields, return a list of only the values associated with those fields.\n  A single field returns a list of values, multiple fields returns a list of value tuples.\n\n\n.. _`simple tables`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#simple-tables\n',
    'author': 'Brad Brown',
    'author_email': 'brad@bradsbrown.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jolly-good-toolbelt.github.io/tableread/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
