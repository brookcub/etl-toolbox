etl-toolbox
===========

   Useful ETL functions for Python

**etl-toolbox** is a Python library of simple but powerful functions for ETL and
data cleaning. It contains tools that are useful for nearly any ETL pipeline,
with a specific focus on the data variety challenges that arise when compiling
data from many sources.

.. image:: https://img.shields.io/github/workflow/status/brookcub/etl-toolbox/Tests?logo=github
   :alt: GitHub Build Status
   :target: https://github.com/brookcub/etl-toolbox/actions?query=workflow%3ATests+branch%3Amaster

.. image:: https://codecov.io/gh/brookcub/etl-toolbox/branch/master/graph/badge.svg
   :alt: Coverage
   :target: https://codecov.io/gh/brookcub/etl-toolbox

.. image:: https://img.shields.io/readthedocs/etl-toolbox?label=Read%20the%20Docs&logo=Read%20the%20Docs
   :alt: Read the Docs
   :target: https://etl-toolbox.readthedocs.io/en/latest/

.. image:: https://img.shields.io/pypi/v/etl-toolbox.svg?color=ffa313
   :alt: PyPI Version
   :target: https://pypi.python.org/pypi/etl-toolbox

.. image:: https://img.shields.io/pypi/pyversions/etl-toolbox.svg?color=0882ac
   :alt: Supported Python versions
   :target: https://pypi.python.org/pypi/etl-toolbox

.. image:: https://img.shields.io/pypi/l/etl-toolbox.svg?color=0882ac
   :alt: License
   :target: https://pypi.python.org/pypi/etl-toolbox

Features
--------

- Standardize various null-indicating values (``'blank'``, ``'none'``, ``'null'``, etc) to Python's ``None``
- Trim, condense, and standardize whitespace with a single function
- Locate and rename column labels in messy files

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. _PyPI: http://pypi.python.org/pypi/etl-toolbox/
.. _pip: https://pip.pypa.io/en/stable/quickstart/

Install from PyPI_ using pip_::

      $ pip install etl_toolbox

Usage
~~~~~

>>> import pandas as pd
>>>
>>> df = pd.read_csv('./test_data/bad-data.csv')
>>> df  # doctest:+SKIP
         Unnamed: 0           Unnamed: 1            Unnamed: 2    Unnamed: 3 Unnamed: 4
0      created by:   Brookcub Industries  for testing purposes           NaN        NaN
1             date:           2020-06-07                3 rows  some columns        NaN
2               NaN                  NaN                   NaN           NaN        NaN
3             Cust.             EML-addr                On          phn-nmbr       col5
4     Golden jackal    c.aureus@mail.com              03/04/14      333-4444      blank
5  Pie, rufous tree                 none                   NaN      222-3333      empty
6   Vulture, bengal              blocked              06/01/15      777-7777       none
7       Arctic tern  s_paradise@mail.com              01/28/16           NaN        NaN
8   Eurasian badger  meles@othermail.net         notavailable            NaN        NaN
9   Grant's gazelle   grant@randmail.com                     -           NaN        NaN

Find and standardize column labels using a dictionary of the expected values:

>>> from etl_toolbox.dataframe_functions import find_column_labels
>>> from etl_toolbox.mapping_functions import map_labels
>>>
>>> fingerprint_map = {
...     'cust': 'Name',
...     'emladdr': 'Email',
...     'on': 'Date',
...     'phnnmbr': 'Phone'
... }
>>>
>>> find_column_labels(df, fingerprint_map)
>>> df
              Cust.             EML-addr         On      phn-nmbr   col5
0     Golden jackal    c.aureus@mail.com       03/04/14  333-4444  blank
1  Pie, rufous tree                 none            NaN  222-3333  empty
2   Vulture, bengal              blocked       06/01/15  777-7777   none
3       Arctic tern  s_paradise@mail.com       01/28/16       NaN    NaN
4   Eurasian badger  meles@othermail.net  notavailable        NaN    NaN
5   Grant's gazelle   grant@randmail.com              -       NaN    NaN
>>>
>>> df.columns = map_labels(df.columns, fingerprint_map)
>>> df
               Name                Email           Date     Phone    NaN
0     Golden jackal    c.aureus@mail.com       03/04/14  333-4444  blank
1  Pie, rufous tree                 none            NaN  222-3333  empty
2   Vulture, bengal              blocked       06/01/15  777-7777   none
3       Arctic tern  s_paradise@mail.com       01/28/16       NaN    NaN
4   Eurasian badger  meles@othermail.net  notavailable        NaN    NaN
5   Grant's gazelle   grant@randmail.com              -       NaN    NaN

Standardize null values and remove empty rows/columns:

>>> from etl_toolbox.dataframe_functions import dataframe_clean_null
>>>
>>> dataframe_clean_null(df)
>>> df
               Name                Email      Date     Phone
0     Golden jackal    c.aureus@mail.com  03/04/14  333-4444
1  Pie, rufous tree                  NaN       NaN  222-3333
2   Vulture, bengal                  NaN  06/01/15  777-7777
3       Arctic tern  s_paradise@mail.com  01/28/16       NaN
4   Eurasian badger  meles@othermail.net       NaN       NaN
5   Grant's gazelle   grant@randmail.com       NaN       NaN

Or clean individual data values:

>>> from etl_toolbox.cleaning_functions import clean_whitespace
>>>
>>> clean_whitespace(''' 123   abc 456
...                               def\t\t 789\t''')
'123 abc 456 def 789'

.. docs-exclusion-marker-start

Documentation
-------------

Full documentation is hosted at `etl-toolbox.readthedocs.io <https://etl-toolbox.readthedocs.io>`_.

.. docs-exclusion-marker-end

Contributing
------------

.. _Open an issue: https://github.com/brookcub/etl-toolbox/issues/new
.. _issue tracker: https://github.com/brookcub/etl-toolbox/issues
.. _this repository: https://github.com/brookcub/etl-toolbox/
.. _the Stack Overflow guide: https://stackoverflow.com/help/minimal-reproducible-example
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Flake8: https://flake8.pycqa.org/en/latest/

Contributions are appreciated! There are multiple ways to contribute:

Bug Reports
~~~~~~~~~~~

Bug reports help make this library more robust. A good bug report should include:

#. A clear description of the problem (the *expected* behavior vs the *actual* behavior)
#. A minimal, reproducible example (see `the Stack Overflow guide`_)
#. The platform and versions involved (operating system, Python version, ``etl-toolbox`` version, ``pandas``/``numpy`` version if applicable, etc)

Submit bug reports with the `issue tracker`_ on GitHub.

Feature Requests
~~~~~~~~~~~~~~~~

`Open an issue`_ to discuss features you'd like to see added to etl-toolbox.

Pull Requests
~~~~~~~~~~~~~

Follow these steps for submitting pull requests:

#. Find an issue or feature on the `issue tracker`_.
#. Fork `this repository`_ on GitHub and make changes in a branch.
#. Add tests to confirm that the bugfix/feature works as expected.
#. Run the entire test suite and coverage report with ``pytest --doctest-modules --doctest-glob=*.rst --cov=etl_toolbox --ignore=docs/conf.py``. Make sure text coverage is 100% and all tests are passing.
#. Submit a pull request.

The code style for etl-toolbox mostly follows PEP8_. A linter like Flake8_ is recommended for double checking new contributions.

Release History
---------------

-  0.0.2

   -  Add GitHub continuous integration
   -  Add project links and badges to readme and PyPI metadata
   -  Fix bug in ``merge_columns_by_label()`` that raises a ``ValueError`` if ``df`` has multiple columns labeled ``None``

-  0.0.1

   -  Initial release
