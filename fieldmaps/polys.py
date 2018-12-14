"""Polygon maps."""

from .settings import continuous_palette, discrete_palette
from .utils import AxesUpdater, DataContainer


def poly_cont(data, verts, ax=None, palette=continuous_palette, lower=None, upper=None, **kwargs):  # noqa
    """Plot a map from continous values tied to polygons.

    Parameters
    ----------
    data : one-dim sequence
        Variable to be plotted. If the sequence is a masked array,
        masked values will be treated as missing data.
    verts : sequence
        Sequence of polygon coordinates. See
        `matplotlib.collections.PolyCollection` for more information.
    ax : matplotlib Axes, optional
        The axis onto which the plot will be drawn. If not provided,
        a new axis will be created.
    palette : None or string, optional
        Name of palette (colormap) to use or None to use the current
        palette. If not provided, the package's default palette will
        be used.
    lower : numeric, optional
        If provided, the lower bound for which data should be displayed.
    upper : numeric, optional
        If provided, the upper bound for which data should be displayed.
    kwargs
        Keyword arguments to be passed to
        `matplotlib.collections.PolyCollection`.

    Returns
    -------
    matplotlib Axes
    """

    container = DataContainer.from_continuous(
        data,
        palette,
        lower=lower,
        upper=upper)
    updater = AxesUpdater.from_continuous(container, ax=ax, **kwargs)
    collection = updater.add_polygons(verts)
    updater.add_colorbar(collection)
    return updater.ax

def poly_discrete(data, verts, ax=None, palette=discrete_palette, **kwargs):
    """Plot a map from discrete values tied to polygons.

    Parameters
    ----------
    data : one-dim sequence
        Variable to be plotted. If the sequence is a masked array,
        masked values will be treated as missing data.
    verts : sequence
        Sequence of polygon coordinates. See
        `matplotlib.collections.PolyCollection` for more information.
    ax : matplotlib Axes, optional
        The axis onto which the plot will be drawn. If not provided,
        a new axis will be created.
    palette : None or string, optional
        Name of palette (colormap) to use or None to use the current
        palette. If not provided, the package's default palette will
        be used.
    kwargs
        Keyword arguments to be passed to
        `matplotlib.collections.PolyCollection`.

    Returns
    -------
    matplotlib Axes
    """

    container = DataContainer.from_discrete(data, palette)
    updater = AxesUpdater.from_discrete(container, ax=ax, **kwargs)
    collection = updater.add_polygons(verts)
    updater.add_colorbar(collection)
    return updater.ax
