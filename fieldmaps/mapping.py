"""Handle discrete/categorical data."""

from collections import OrderedDict
from matplotlib.colors import BoundaryNorm, ListedColormap

import matplotlib.cm as cm
import numpy as np


# Arbitrary - this is the maximum number of ticks on a colorbar + 1.
# Will be masked out, so the actual value isn't important.
_fill = 1000
_dtype = np.uint16


def mk_internal_map(x):
    # Map input data to integers >= 0 such that all
    # are strictly ascending and are uniformly spaced.
    # These properties are all necessary so that the
    # colorbar labels will be correct.
    data_values = np.sort(np.unique(x))
    return OrderedDict((value, i) for i, value in enumerate(data_values))

def internal_array(x, pairs):
    # Create array that mirrors the input array, but with
    # internal data values.
    arr = np.fromiter(
        (pairs.get(value, _fill) for value in x.ravel()),
        dtype=_dtype,
        count=x.size)
    return arr.reshape(x.shape)

def create_mapped(x):
    if not isinstance(x, np.ma.MaskedArray):
        mask = np.zeros(x.shape, dtype=np.bool)
        x = np.ma.masked_array(x, mask)

    # Only use good data to create the internal data so that
    # when masked values are removed the colorbar will still
    # be accurate.
    data = x.data[~x.mask]
    pairs = mk_internal_map(data)
    arr = internal_array(x.data, pairs)

    # matplotlib will take masked values as "bad" data.
    mock = np.ma.masked_array(arr, x.mask)
    return pairs, mock

def discrete_norm(x):
    assert isinstance(x, tuple)

    # The last bound doesn't show up in the colorbar, so an offset needs to be
    # added. This will then add a tick label at the end of the colorbar that
    # doesn't correspond to a color! This must be fixed in the colorbar (see
    # `add_discrete_labels`).
    boundaries = x + (max(x) + 1,)
    norm = BoundaryNorm(boundaries, ncolors=len(x))
    return norm

# TODO: is this necessary at all?
def discrete_cmap(x, palette):
    colors = cm.get_cmap(palette)(x)
    colormap = ListedColormap(colors)
    return colormap

def add_discrete_labels(cbar, labels):
    # Set labels in the middle of the color segment.
    n = len(labels)
    cbar.set_ticks(np.arange(n) + .5)
    cbar.set_ticklabels(labels)
    return cbar
