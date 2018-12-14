fieldmaps
=========

Fieldmaps is a Python package for visualizing geographic data. It provides a
high-level API for plotting spatially cohesive data represented by raster,
polygon and point geometries.


Development
-----------

Use `tox` to lint and run tests for a given python version

```
$ tox -e py37
```

For a more detailed coverage report, generate the report as HTML and open it in
a browser

```
$ tox -e py37 -- --cov-report html:cov_html
$ open cov_html/index.html
```

`tox` can also be used to generate a local version of the docs (note that you
will need an internet connection to fetch sample data that is required to build
the docs)

```
$ tox -e docs
$ open .tox/html/index.html
```
