"""Internal utility functions."""

from matplotlib.colors import BoundaryNorm, Normalize
from matplotlib.pyplot import gca

import numpy as np
import matplotlib.cm as cm
import matplotlib.collections as collections

from .settings import color_missing, im_settings, point_settings
from . import mapping


def get_extend(norm):
    if isinstance(norm, BoundaryNorm):
        # Norm used for a discrete mapping.
        return "neither"

    # Determine `extend` argument to `figure.colorbar` that
    # corresponds to the norm.
    if norm.vmin is not None and norm.vmax is not None:
        return "both"
    elif norm.vmin is not None and norm.vmax is None:
        return "min"
    elif norm.vmin is None and norm.vmax is not None:
        return "max"
    return "neither"

def mask(data):
    # TODO: pass through if already masked?
    return np.ma.MaskedArray(data, np.isnan(data) | ~np.isfinite(data))

class DataContainer(object):
    """Hold the internal representation of the data."""

    def __init__(self, data, colormap, norm, ticklabels):
        self.data = data
        self.colormap = colormap
        self.colormap.set_bad(color_missing)
        self.norm = norm
        self.ticklabels = ticklabels

    @classmethod
    def from_discrete(cls, data, palette):
        data = np.asanyarray(data)
        pairs, mock = mapping.create_mapped(data)
        ticklabels, internal_data = zip(*pairs.items())
        norm = mapping.discrete_norm(internal_data)
        colormap = mapping.discrete_cmap(internal_data, palette)
        return cls(mock, colormap, norm, ticklabels)

    @classmethod
    def from_continuous(cls, data, palette, *, lower=None, upper=None):
        data = np.asanyarray(data)
        if not isinstance(data, np.ma.MaskedArray):
            data = mask(data)

        norm = Normalize(lower, upper)
        colormap = cm.get_cmap(palette)
        return cls(data, colormap, norm, None)

class AxesUpdater(object):
    """Draw on the axes."""

    def __init__(self, container, ax, plot_kwds):
        if ax is None:
            ax = gca()

        self.container = container
        self.ax = ax
        self.plot_kwds = plot_kwds

    @classmethod
    def from_discrete(cls, container, ax=None, **kwds):
        plot_kwds = {
            **kwds,
            "cmap": container.colormap,
            "norm": container.norm,
        }
        return cls(container, ax, plot_kwds)

    @classmethod
    def from_continuous(cls, container, ax=None, **kwds):
        # Some plotting methods (e.g. scatter) will modify
        # `norm` in-place if either `vmin` or `vmax` are
        # None. To avoid this, the `vmin` and `vmax` values
        # are passed to normalize the data, instead of using
        # `norm`.
        plot_kwds = {
            **kwds,
            "cmap": container.colormap,
            "vmin": container.norm.vmin,
            "vmax": container.norm.vmax,
        }
        return cls(container, ax, plot_kwds)

    def add_points(self, xy):
        kwds = {**point_settings, **self.plot_kwds}
        # `scatter will filter out any masked values. To ensure
        # that they're plotted, pass the color mapping information
        # directly to the collection after calling `scatter` and the
        # colors will be updated when rendering the figure.
        collection = self.ax.scatter(*xy.T, c=None, **kwds)
        collection.set_array(self.container.data)
        collection.set_cmap(self.container.colormap)
        collection.set_norm(self.container.norm)
        return collection

    def add_polygons(self, verts):
        # PolyCollection does not allow `vmin`/`vmax`,
        # and `norm` is already passed.
        kwds = {
            k: v for k, v in self.plot_kwds.items()
            if k not in ("vmin", "vmax", "norm")
        }
        p = collections.PolyCollection(
            verts,
            array=self.container.data,
            norm=self.container.norm,
            **kwds)
        self.ax.add_collection(p)
        self.ax.autoscale_view()
        return p

    def add_raster(self):
        kwds = {**im_settings, **self.plot_kwds}
        return self.ax.imshow(self.container.data, **kwds)

    def add_colorbar(self, collection):
        ax = self.ax
        extend = get_extend(self.container.norm)
        colorbar = ax.figure.colorbar(collection, ax=ax, extend=extend)

        ticklabels = self.container.ticklabels
        if ticklabels is not None:
            mapping.add_discrete_labels(colorbar, labels=ticklabels)

        return
