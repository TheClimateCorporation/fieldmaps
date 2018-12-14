from fieldmaps.settings import color_missing
from fieldmaps.utils import AxesUpdater, DataContainer, get_extend, mask
from matplotlib.colors import Normalize

import matplotlib.pyplot as plt
import numpy as np
import pytest


@pytest.fixture(autouse=True)
def close_plots():
    plt.close("all")
    return

def get_ax():
    _, ax = plt.subplots()
    return ax

@pytest.mark.parametrize("vmin,vmax,expected", [
    (0, 1, "both"),
    (0, None, "min"),
    (None, 1, "max"),
    (None, None, "neither"),
])
def test_extend(vmin, vmax, expected):
    norm = Normalize(vmin=vmin, vmax=vmax)
    assert get_extend(norm) == expected

def test_mask():
    data = np.array([np.nan, 2, 3, np.inf, 5, -np.inf])
    expected_mask = np.array([True, False, False, True, False, True])

    masked = mask(data)
    assert np.all(masked.mask == expected_mask)

    masked_data = np.ma.masked_array([1, 2, 3], [True, False, False])
    remasked = mask(masked_data)
    assert np.all(remasked == masked_data)

class TestDataContainerContinuous(object):
    palette = "PiYG"

    def test_raster(self):
        data = np.array([[np.inf, np.nan], [3, 4]])
        expected_mask = np.array([[True, True], [False, False]])

        container = DataContainer.from_continuous(
            data,
            self.palette,
            lower=0,
            upper=1)

        assert isinstance(container.data, np.ma.MaskedArray)
        assert np.all(container.data.mask == expected_mask)
        assert hasattr(container, "colormap")
        assert container.norm.vmin == 0
        assert container.norm.vmax == 1
        assert container.ticklabels is None

    def test_1d(self):
        data = np.array([np.inf, np.nan, 3, 4])
        expected_mask = np.array([True, True, False, False])

        container = DataContainer.from_continuous(
            data,
            self.palette,
            lower=0,
            upper=1)

        assert isinstance(container.data, np.ma.MaskedArray)
        assert np.all(container.data.mask == expected_mask)
        assert hasattr(container, "colormap")
        assert container.norm.vmin == 0
        assert container.norm.vmax == 1
        assert container.ticklabels is None

class TestDataContainerDiscrete(object):
    palette = "tab10"

    def test_raster(self):
        data = np.array([["a", "a"], ["b", "b"]])
        expected_mask = np.array([[False, False], [False, False]])

        container = DataContainer.from_discrete(data, self.palette)

        assert isinstance(container.data, np.ma.MaskedArray)
        assert container.data.dtype == np.uint16
        assert np.all(container.data.mask == expected_mask)
        assert container.colormap.N == 2
        assert len(container.ticklabels) == 2

    def test_1d(self):
        data = np.array(["a", "a", "b", "b"])
        expected_mask = np.array([False, False, False, False])

        container = DataContainer.from_discrete(data, self.palette)

        assert isinstance(container.data, np.ma.MaskedArray)
        assert container.data.dtype == np.uint16
        assert np.all(container.data.mask == expected_mask)
        assert container.colormap.N == 2
        assert len(container.ticklabels) == 2

class TestAxesUpdater(object):
    continuous_palette = "PiYG"
    discrete_palette = "tab10"

    @pytest.mark.parametrize("ax", [get_ax(), None], ids=["given_ax", "no_ax"])
    def test_from_continuous(self, ax):
        lower = 0
        upper = 1
        container = DataContainer.from_continuous(
            np.arange(4),
            self.continuous_palette,
            lower=lower,
            upper=upper)
        updater = AxesUpdater.from_continuous(container, ax, random_kwd="hi")

        if ax is None:
            assert updater.ax is plt.gca()
        else:
            assert updater.ax is ax

        assert updater.container is container
        assert updater.plot_kwds["cmap"] == container.colormap
        assert updater.plot_kwds["vmin"] == lower
        assert updater.plot_kwds["vmax"] == upper
        assert updater.plot_kwds["random_kwd"] == "hi"

    @pytest.mark.parametrize("ax", [get_ax(), None], ids=["given_ax", "no_ax"])
    def test_from_discrete(self, ax):
        container = DataContainer.from_discrete(
            np.arange(4),
            self.discrete_palette)
        updater = AxesUpdater.from_discrete(container, ax, random_kwd="hi")

        if ax is None:
            assert updater.ax is plt.gca()
        else:
            assert updater.ax is ax

        assert updater.container is container
        assert updater.plot_kwds["cmap"] == container.colormap
        assert updater.plot_kwds["norm"] == container.norm
        assert updater.plot_kwds["random_kwd"] == "hi"

    @staticmethod
    def assert_masked_colors(masked_data, collection):
        # The collection's colors may not have been set yet, so we force them
        # to be updated, without rendering the figure.
        collection.update_scalarmappable()
        colors = collection.get_facecolors()

        # If alpha is set, Matplotlib will override the alpha band of all
        # colors with it, regardless of whether the value is bad/masked or
        # not.
        masked_color = np.array(color_missing)
        alpha = collection.get_alpha()
        if alpha is not None:
            masked_color[-1] = alpha

        for rgba, masked in zip(colors, masked_data.mask):
            if masked:
                assert np.all(rgba == masked_color)

    @pytest.mark.parametrize("continuous", [True, False], ids=["continuous", "discrete"])  # noqa
    @pytest.mark.parametrize("mask", [True, False], ids=["masked", "unmasked"])
    def test_add_points(self, continuous, mask):
        data = np.arange(3)
        coords = np.array([[0, 0], [1, 1], [2, 2]])
        alpha = .5

        if mask:
            data = np.ma.masked_array(data, [True, False, True])

        if continuous:
            container = DataContainer.from_continuous(
                data,
                self.continuous_palette,
                lower=0,
                upper=1)
            updater = AxesUpdater.from_continuous(container, alpha=alpha)
        else:
            container = DataContainer.from_discrete(
                data,
                self.discrete_palette)
            updater = AxesUpdater.from_discrete(container, alpha=alpha)

        collection = updater.add_points(coords)
        assert collection.axes is updater.ax
        assert collection.get_cmap() == container.colormap
        assert collection.norm.vmin == container.norm.vmin
        assert collection.norm.vmax == container.norm.vmax
        assert collection.get_alpha() == alpha
        assert np.all(collection.get_array() == container.data)
        assert np.all(collection.get_offsets() == coords)

        # Internal data always has a mask.
        self.assert_masked_colors(container.data, collection)

    @pytest.mark.parametrize("continuous", [True, False], ids=["continuous", "discrete"])  # noqa
    @pytest.mark.parametrize("mask", [True, False], ids=["masked", "unmasked"])
    def test_add_polygons(self, continuous, mask):
        data = np.arange(3)
        vert = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
        verts = np.array([vert, vert, vert])

        if mask:
            data = np.ma.masked_array(data, [True, False, True])

        if continuous:
            container = DataContainer.from_continuous(
                data,
                self.continuous_palette)
            updater = AxesUpdater.from_continuous(container)
        else:
            container = DataContainer.from_discrete(
                data,
                self.discrete_palette)
            updater = AxesUpdater.from_discrete(container)

        collection = updater.add_polygons(verts)

        assert collection.axes is updater.ax
        assert collection.get_cmap() == container.colormap
        assert collection.norm == container.norm
        assert np.all(collection.get_array() == container.data)
        assert len(collection.get_paths()) == len(verts)

        # Internal data always has a mask.
        self.assert_masked_colors(container.data, collection)

    @pytest.mark.parametrize("continuous", [True, False], ids=["continuous", "discrete"])  # noqa
    def test_add_raster(self, continuous):
        data = np.array([[0, 1], [2, 3]])
        alpha = .5

        if continuous:
            container = DataContainer.from_continuous(
                data,
                self.continuous_palette,
                lower=0,
                upper=1)
            updater = AxesUpdater.from_continuous(container, alpha=alpha)
        else:
            container = DataContainer.from_discrete(
                data,
                self.discrete_palette)
            updater = AxesUpdater.from_discrete(container, alpha=alpha)

        collection = updater.add_raster()

        assert collection.axes is updater.ax
        assert collection.get_cmap() == container.colormap
        assert collection.norm.vmin == container.norm.vmin
        assert collection.norm.vmax == container.norm.vmax
        assert collection.get_alpha() == alpha
        assert np.all(collection.get_array() == container.data)

    def test_add_colorbar_continuous(self):
        fig, ax = plt.subplots()
        data = np.arange(3)
        collection = ax.scatter(data, data, c=data)
        container = DataContainer.from_continuous(
            data,
            self.continuous_palette)
        updater = AxesUpdater(container, ax, {})
        updater.add_colorbar(collection)

        assert len(fig.axes) == 2, "Colorbar wasn't added to figure"
        assert hasattr(ax.collections[0], "colorbar")

    def test_add_colorbar_discrete(self):
        fig, ax = plt.subplots()
        data = np.arange(3)
        colors = data.copy()
        container = DataContainer.from_discrete(data, self.discrete_palette)
        collection = ax.scatter(
            data,
            data,
            c=colors,
            cmap=container.colormap,
            norm=container.norm)
        updater = AxesUpdater(container, ax, {})
        updater.add_colorbar(collection)

        assert len(fig.axes) == 2, "Colorbar wasn't added to figure"
        assert hasattr(ax.collections[0], "colorbar")

        cbar = ax.collections[0].colorbar
        assert cbar.extend == "neither"
        assert len(cbar.get_ticks()) == len(colors)
