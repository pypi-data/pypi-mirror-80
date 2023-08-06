=============================
pyfb-company
=============================

.. image:: https://badge.fury.io/py/pyfb-company.svg
    :target: https://badge.fury.io/py/pyfb-company

.. image:: https://travis-ci.org/mwolff44/pyfb-company.svg?branch=master
    :target: https://travis-ci.org/mwolff44/pyfb-company

.. image:: https://codecov.io/gh/mwolff44/pyfb-company/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mwolff44/pyfb-company

Company package for pyfreebilling application

Documentation
-------------

The full documentation is at https://pyfb-company.readthedocs.io.

Quickstart
----------

Install pyfb-company::

    pip install pyfb-company

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'pyfb_company.apps.PyfbCompanyConfig',
        ...
    )

Add pyfb-company's URL patterns:

.. code-block:: python

    from pyfb_company import urls as pyfb_company_urls


    urlpatterns = [
        ...
        url(r'^', include(pyfb_company_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

1.2.0 (2020-09-17)
++++++++++++++++++

* Addition of a parameter to authorize the update of the balance 

1.1.0 (2020-09-14)
++++++++++++++++++

* Add a settings to block call if credit limit is reached

1.0.0 (2020-05-21)
++++++++++++++++++

* update dependencies


0.9.0 (2018-12-10)
++++++++++++++++++

* First release on PyPI.


