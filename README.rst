fieldmaps
=========

.. image:: https://travis-ci.org/TheClimateCorporation/fieldmaps.svg?branch=master
   :target: https://travis-ci.org/TheClimateCorporation/fieldmaps

.. image:: https://readthedocs.org/projects/fieldmaps/badge/?version=latest
   :target: https://fieldmaps.readthedocs.io/en/latest/?badge=latest

.. start-introduction-marker

Fieldmaps is a Python package for visualizing geographic data. It provides a
high-level API for plotting spatially cohesive data represented by raster,
polygon and point geometries.

.. end-introduction-marker


Installation
------------

Install from source

.. code-block:: bash

   $ python setup.py install


Development
-----------

Use ``tox`` to lint and run tests for a given python version

.. code-block:: bash

   $ tox -e py37

For a more detailed coverage report, generate the report as HTML and open it in
a browser

.. code-block:: bash

   $ tox -e py37 -- --cov-report html:cov_html
   $ open cov_html/index.html

``tox`` can also be used to generate a local version of the docs (note that you
will need an internet connection to fetch sample data that is required to build
the docs)

.. code-block:: bash

   $ tox -e docs
   $ open .tox/html/index.html
