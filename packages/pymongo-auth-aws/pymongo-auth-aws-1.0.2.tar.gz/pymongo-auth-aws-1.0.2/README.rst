================
pymongo-auth-aws
================
:Info: MONGODB-AWS authentication support for PyMongo. See
       `GitHub <https://github.com/mongodb/pymongo-auth-aws>`_
       for the latest source.
:Author: Shane Harvey

About
=====

MONGODB-AWS authentication support for PyMongo. pymongo-auth-aws uses
`botocore`_ and `requests`_.

Support / Feedback
==================

For issues with, questions about, or feedback for pymongo-auth-aws, please look into
our `support channels <http://www.mongodb.org/about/support>`_. Please
do not email any of the pymongo-auth-aws developers directly with issues or
questions - you're more likely to get an answer on the `MongoDB Community Forums`_.

Bugs / Feature Requests
=======================

Think you’ve found a bug? Want to see a new feature in pymongo-auth-aws?
Please open a case in our issue management tool, JIRA:

- `Create an account and login <https://jira.mongodb.org>`_.
- Navigate to `the PYTHON project <https://jira.mongodb.org/browse/PYTHON>`_.
- Click **Create Issue** - Please provide as much information as possible about the issue type and how to reproduce it.

Bug reports in JIRA for all driver projects (i.e. PYTHON, CSHARP, JAVA) and the
Core Server (i.e. SERVER) project are **public**.

How To Ask For Help
-------------------

Issues with, questions about, or feedback for pymongo-auth-aws should be sent
to the `MongoDB Community Forums`_.

Please include all of the following information when opening an issue:

- Detailed steps to reproduce the problem, including full traceback, if possible.
- The exact python version used, with patch level::

  $ python -c "import sys; print(sys.version)"

- The exact version of pymongo-auth-aws used::

  $ python -c "import pymongo-auth-aws; print(pymongo_auth_aws.__version__)"

- The exact version of PyMongo used::

  $ python -c "import pymongo; print(pymongo.version); print(pymongo.has_c())"

- The operating system and version (e.g. Windows 10, OSX 10.15, ...)
- Web framework or asynchronous network library used, if any, with version (e.g.
  Django 3.0, mod_wsgi 4.7.1, gevent 20.5.2, Tornado 6.0.4, ...)

Security Vulnerabilities
------------------------

If you've identified a security vulnerability in a driver or any other
MongoDB project, please report it according to the `instructions here
<http://docs.mongodb.org/manual/tutorial/create-a-vulnerability-report>`_.

Installation
============

pymongo-auth-aws can be installed with `pip <http://pypi.python.org/pypi/pip>`_::

  $ python -m pip install pymongo-auth-aws
  $ python -c "import pymongo_auth_aws; print(pymongo_auth_aws.__version__)"
  1.0.0

Installing from source
----------------------

To install pymongo-auth-aws from source::

  $ git clone git@github.com:mongodb/pymongo-auth-aws.git
  $ python -m pip install ./pymongo-auth-aws

Dependencies
============

pymongo-auth-aws supports CPython 2.7, 3.4+, PyPy, and PyPy3.5+.

pymongo-auth-aws requires `botocore`_ and `requests`_.

Testing
=======

To run the test suite::

  $ python setup.py test

.. _MongoDB Community Forums:
   https://developer.mongodb.com/community/forums/tag/python-driver

.. _botocore: https://pypi.org/project/botocore/

.. _requests: https://pypi.org/project/requests/
