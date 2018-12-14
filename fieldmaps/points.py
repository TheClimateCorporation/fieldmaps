"""Scatterplot maps."""

from .settings import continuous_palette, discrete_palette
from .utils import AxesUpdater, DataContainer


def point_cont(data, coords, ax=None, palette=continuous_palette, lower=None, upper=None, **kwargs):  # noqa
    """Plot a scatterplot map with continuous values.

    Parameters
    ----------
    data : one-dim sequence
        Variable to be plotted. If the sequence is a masked array,
        masked values will be treated as missing data.
    coords : array, shape (n, 2)
        Array of coordinates, with the first column giving the
        x-coordinates and the second giving the y-coordinates.
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
        Keyword arguments to be passed to `scatter`.

    Returns
    -------
    matplotlib Axes
    """

    if coords.ndim != 2:
        raise ValueError("`coords` must be a 2-dim array")
    if coords.shape[1] != 2:
        raise ValueError("`coords` must be an array of shape (n, 2)")

    container = DataContainer.from_continuous(
        data,
        palette,
        lower=lower,
        upper=upper)
    updater = AxesUpdater.from_continuous(container, ax=ax, **kwargs)
    collection = updater.add_points(coords)
    updater.add_colorbar(collection)
    return updater.ax

def point_discrete(data, coords, ax=None, palette=discrete_palette, **kwargs):
    """Plot a scatterplot map with discrete values.

    Parameters
    ----------
    data : one-dim sequence
        Variable to be plotted. If the sequence is a masked array,
        masked values will be treated as missing data.
    coords : array, shape (n, 2)
        Array of coordinates, with the first column giving the
        x-coordinates and the second giving the y-coordinates.
    ax : matplotlib Axes, optional
        The axis onto which the plot will be drawn. If not provided,
        a new axis will be created.
    palette : None or string, optional
        Name of palette (colormap) to use or None to use the current
        palette. If not provided, the package's default palette will
        be used.
    kwargs
        Keyword arguments to be passed to `scatter`.

    Returns
    -------
    matplotlib Axes
    """

    if coords.ndim != 2:
        raise ValueError("`coords` must be a 2-dim array")
    if coords.shape[1] != 2:
        raise ValueError("`coords` must be an array of shape (n, 2)")

    container = DataContainer.from_discrete(data, palette)
    updater = AxesUpdater.from_discrete(container, ax=ax, **kwargs)
    collection = updater.add_points(coords)
    updater.add_colorbar(collection)
    return updater.ax
