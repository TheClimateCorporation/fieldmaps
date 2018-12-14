from .settings import continuous_palette, discrete_palette
from .utils import AxesUpdater, DataContainer


def raster_cont(data, ax=None, palette=continuous_palette, lower=None, upper=None, **kwargs):  # noqa
    """Plot a raster with continuous values.

    Parameters
    ----------
    data : ndarray
        Raster to be plotted. If the raster is a masked array, masked
        values will be treated as missing data.
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
        Keyword arguments to be passed to `imshow`.

    Returns
    -------
    matplotlib Axes
    """

    if data.ndim > 2:
        raise ValueError("Only 2-dim rasters are supported")

    container = DataContainer.from_continuous(
        data,
        palette,
        lower=lower,
        upper=upper)
    updater = AxesUpdater.from_continuous(container, ax=ax, **kwargs)
    collection = updater.add_raster()
    updater.add_colorbar(collection)
    return updater.ax

def raster_discrete(data, ax=None, palette=discrete_palette, **kwargs):
    """Plot a raster with discrete data.

    Parameters
    ----------
    data : ndarray, shape (n, m)
        Raster to be plotted. If the raster is a masked array, masked
        values will be treated as missing data.
    ax : matplotlib Axes, optional
        The axis onto which the plot will be drawn. If not provided,
        a new axis will be created.
    palette : None or string, optional
        Name of palette (colormap) to use or None to use the current
        palette. If not provided, the package's default palette will
        be used.
    kwargs
        Keyword arguments to be passed to `imshow`.

    Returns
    -------
    matplotlib Axes
    """

    if data.ndim > 2:
        raise ValueError("Only 2-dim rasters are supported")

    container = DataContainer.from_discrete(data, palette)
    updater = AxesUpdater.from_discrete(container, ax=ax, **kwargs)
    collection = updater.add_raster()
    updater.add_colorbar(collection)
    return updater.ax
