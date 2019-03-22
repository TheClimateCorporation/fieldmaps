Usage
=====

Fieldmaps strives to make plotting fields as painless as possible by providing
a consistent API across different geographic and data types. Maps are created
such that the *x* and *y* axes give the Easting and Northing coordinates,
respectively, and the measurement variable is displayed as the color. Raster,
polygon and point geographic types are supported.

Mapping functions are organized as a matrix, where the geographic type is given
as the prefix of the function name and the function name's suffix gives the data
type of the measurement variable. The data type ``discrete`` covers both integer
and categorical types.

.. list-table:: Mapping Functions
   :widths: auto
   :header-rows: 1

   * - Data/Geography
     - Raster
     - Polygon
     - Point
   * - Continuous
     - :func:`~fieldmaps.raster_cont`
     - :func:`~fieldmaps.poly_cont`
     - :func:`~fieldmaps.point_cont`
   * - Discrete/Categorical
     - :func:`~fieldmaps.raster_discrete`
     - :func:`~fieldmaps.poly_discrete`
     - :func:`~fieldmaps.point_discrete`

See :ref:`examples` for how to use the mapping functions.


Colormap
--------

The colormaps used for the measurement variable are set as default arguments to
provide a default theme. They may be overridden through the ``palette``
argument, which takes the name of a registered ``matplotlib`` colormap. Note
that the default colormap for discrete/categorical data can only handle up to 20
unique values.


Masked Arrays
-------------

Passing a masked array as the measure variable will cause masked observations to
be set to gray. By default, ``nan`` and ``inf`` values in continuous data will
be masked internally, resulting in the same behavior. To suppress this behavior
for ``inf`` values, a masked array with all mask values set to ``False`` can be
passed, although this is not recommended.

Note that the geographic entities corresponding to the masked observations will
still be drawn. If there are values which should not be in the plot, they must
be filtered out prior to calling the mapping function. Any data that is passed
will be plotted!


Truncation
----------

When working with continuous data, outlier values may stretch the colorbar to
the point where the bulk of the data ends up as a similar hue. One method to
deal with this is by masking the outliers in the input array so that the
colorbar is not extended to include them. An alternative is to tell fieldmaps to
*truncate* the colorbar. This can be achieved through the ``lower`` and/or
``upper`` arguments, which will cause all values below or above their respective
thresholds to be the same color. Truncating the colorbar this way preserves the
color gradient for untruncated values without removing data. 

.. code-block:: python

   fm.point_cont(measure, coords, lower=-1000)
   fm.point_cont(measure, coords, upper=1000)
   fm.point_cont(measure, coords, lower=-1000, upper=1000)


For a visual example of the effects of masking and truncation, see
:ref:`censor-example`.


Working with shapely geometries
-------------------------------

Geographic coordinates are passed following ``matplotlib`` conventions. Although
this is convenient for moving back and forth to ``matplotlib`` functions, it
is less so if using objects that better represent geometries. Fortunately,
it is simple to cast ``shapely`` geometries to the required types.

To convert ``shapely`` polygons to the format required by ``fieldmaps`` (note
that any interiors will not be preserved):

.. code-block:: python

   import numpy as np
   import shapely.wkt

   polygons_wkt = [
       "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
       "POLYGON((0 0, 0 2, 2 2, 2 0, 0 0))",
   ]
   polygons = [shapely.wkt.loads(wkt) for polygon_wkt in polygons_wkt]
   exteriors = [polygon.exterior.coords for polygon in polygons]
   coords = np.array(exteriors)


Converting points is similar:

.. code-block:: python

   import numpy as np
   import shapely.wkt

   points_wkt = [
       "POINT(0 1)",
       "POINT(1 0)",
   ]
   points = [shapely.wkt.loads(wkt) for point_wkt in points_wkt]
   xy = [(point.x, point.y) for point in points]
   coords = np.array(xy)
