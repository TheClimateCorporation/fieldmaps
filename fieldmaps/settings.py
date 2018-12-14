"""Superficial default settings."""

from matplotlib.cm import get_cmap, register_cmap
from matplotlib.colors import ListedColormap
from numpy import array


#: Default color palette for continuous data.
continuous_palette = "YlGn"
#: Secondary color palette for continuous data.
alternate_palette = "Blues"
#: Default color palette for discrete data.
discrete_palette = "tab20_woven"

continuous_color = (.38601, .73495, .43145)  # 140th color in YlGn
alternate_color = (.28089, .58762, .78508)   # 155th color in Blues
color_missing = (.4, .4, .4, .2)             # Lightgrey.
color_gridlines = (.6, .6, .6, .5)           # Darkgrey.

im_settings = {
    "interpolation": "none",
    "origin": "upper",
}

point_settings = {
    "s": 1,
    "marker": "s"
}

patch_settings = {
    "alpha": 0.5,
    "closed": True,
    "edgecolor": "k",
    "facecolor": "none",
    "fill": False,
    "linestyle": "solid",
    "linewidth": 1
}


def mk_discrete_cmap(name):
    """Modified version of `tab20` palette such that light versions
    of colors are shifted to the end of the cycle.
    """

    tab20 = get_cmap("tab20")
    regular_color_idx = list(range(0, tab20.N, 2))
    light_color_idx = list(range(1, tab20.N, 2))
    colors = [tab20.colors[i] for i in regular_color_idx + light_color_idx]
    return ListedColormap(tuple(colors), name=name)

register_cmap(cmap=mk_discrete_cmap(discrete_palette))

def apply_theme(*axes, grid=False):
    """Update one or more axes with the package theme.

    Each axes is modified in place. If more than one is provided,
    they are returned as a flat array.

    Parameters
    ----------
    *axes : matplotlib Axes
        Axes containing the plot(s) to be modified.
    grid : bool, optional
        Add gridlines to each axes. It is advised to leave
        this as False if using a 3rd-party theme (e.g.
        seaborn's `darkgrid`).

    Returns
    -------
    matplotlib Axes or array of Axes
    """

    for ax in axes:
        ax.set_xlabel("Easting")
        ax.set_ylabel("Northing")

        # Force x and y axes to be equally spaced, as befitting
        # geographic/geometric data. This has potential to create
        # a large amount of whitespace around the data, as an
        # unfortunate side-effect.
        ax.set_aspect("equal", adjustable="datalim")

        # Remove axis ticks and tick labels.
        # Tick labels are not removed with `ax.tick_params`
        # as it leaves the coordinate offset in the corner.
        ax.tick_params(
            axis="both",
            which="both",
            bottom=False,
            top=False,
            left=False,
            right=False)
        ax.set_yticklabels([])
        ax.set_xticklabels([])

    if grid:
        for ax in axes:
            ax.grid(True, color=color_gridlines)

    # Attempt to preserve inputs - matplotlib uses arrays to wrap multiple
    # axes.
    axes = array(axes) if len(axes) > 1 else axes[0]
    return axes
