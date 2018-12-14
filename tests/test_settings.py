import matplotlib.pyplot as plt
import pytest

from fieldmaps import settings


@pytest.fixture(autouse=True)
def close_plots():
    plt.close("all")

def test_discrete_cmap_registered():
    assert settings.discrete_palette in plt.colormaps()

class TestApplyTheme(object):
    @pytest.mark.parametrize(
        "grid, expected_color",
        (
            (True, settings.color_gridlines),
            (False, plt.rcParams["grid.color"]),
        ),
        ids=("grid", "no_grid"))
    def test_single_ax(self, grid, expected_color):
        _, ax = plt.subplots()
        out_ax = settings.apply_theme(ax, grid=grid)

        assert out_ax is ax
        assert out_ax.get_xlabel() == "Easting"
        assert out_ax.get_ylabel() == "Northing"
        assert out_ax.get_aspect() == "equal"
        assert out_ax.get_adjustable() == "datalim"
        assert all(
            gridline.get_color() == expected_color
            for gridline in out_ax.get_xgridlines())
        assert all(
            gridline.get_color() == expected_color
            for gridline in out_ax.get_ygridlines())

    def test_multiple_axes(self):
        _, axes = plt.subplots(1, 2)
        out_axes = settings.apply_theme(*axes)

        assert isinstance(out_axes, type(axes))
        assert len(out_axes) == len(axes)
        assert out_axes[0] is axes[0]
        assert out_axes[1] is axes[1]

    @pytest.mark.xfail
    def test_2d_axes(self):
        _, axes = plt.subplots(2, 2)
        out_axes = settings.apply_theme(*axes)

        assert out_axes.shape == axes.shape
        assert out_axes[0, 0] is axes[0, 0]
        assert out_axes[0, 1] is axes[0, 1]
        assert out_axes[1, 0] is axes[1, 0]
        assert out_axes[1, 1] is axes[1, 1]
