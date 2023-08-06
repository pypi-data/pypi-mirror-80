django-cms-helpers
==================

.. image:: https://img.shields.io/pypi/v/django-cms-helpers.svg
   :target: https://pypi.org/project/django-cms-helpers/
   :alt: Latest Version

.. image:: https://codecov.io/gh/moccu/django-cms-helpers/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/moccu/django-cms-helpers
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-cms-helpers/badge/?version=latest
   :target: https://django-cms-helpers.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/moccu/django-cms-helpers.svg?branch=master
   :target: https://travis-ci.org/moccu/django-cms-helpers


django-cms-helpers is a collection of helpers when working with django-cms.


Features
--------

* templatetag for getting title extension object.
* anylink extension for cms pages.
* boilerplate code for ExtensionToolbar.
* FilerFileField extension to validate file extension and make default_alt_text required.

Requirements
------------

django-cms-helpers supports Python 3 only and requires at least Django 1.11 and django-cms at least 3.4.


Prepare for development
-----------------------

A Python 3.6 interpreter is required in addition to pipenv.

.. code-block:: shell

    $ pipenv install --python 3.6 --dev
    $ pipenv shell
    $ pip install -e .


Now you're ready to run the tests:

.. code-block:: shell

    $ pipenv run py.test


Resources
---------

* `Documentation <https://django-cms-helpers.readthedocs.io>`_
* `Bug Tracker <https://github.com/moccu/django-cms-helpers/issues>`_
* `Code <https://github.com/moccu/django-cms-helpers/>`_
