"""Smoke test top level plotting functions."""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from fieldmaps import (
    point_cont,
    point_discrete,
    poly_cont,
    poly_discrete,
    raster_cont,
    raster_discrete
)


@pytest.fixture(autouse=True)
def close_plots():
    plt.close("all")

continuous_data = np.array([1, 1, 2, 2, 3, 3], dtype=np.float)
continuous_data.setflags(write=False)

categorical_data = np.array(["a", "a", "b", "b", "a", "a"])
categorical_data.setflags(write=False)

discrete_data = np.array([1, 1, 2, 2, 3, 3], dtype=np.uint8)
discrete_data.setflags(write=False)

@pytest.fixture(scope="module")
def mask():
    data = np.array([True, True, False, False, False, False], dtype=np.bool)
    data.setflags(write=False)
    return data

def to_raster(data):
    n = len(data)
    raster = data.reshape(int(n / 2), 2)
    raster.setflags(write=False)
    return raster

@pytest.fixture(scope="module")
def coords():
    xy = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])
    xy.setflags(write=False)
    return xy

@pytest.fixture(scope="module")
def verts():
    vert = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]
    vertices = np.array([vert, vert, vert, vert, vert, vert])
    vertices.setflags(write=False)
    return vertices

point_params = pytest.mark.parametrize(
    "fn, data",
    (
        (point_cont, continuous_data),
        (point_discrete, categorical_data),
        (point_discrete, discrete_data),
    ),
    ids=("continuous", "categorical", "discrete"))

polygon_params = pytest.mark.parametrize(
    "fn, data",
    (
        (poly_cont, continuous_data),
        (poly_discrete, categorical_data),
        (poly_discrete, discrete_data),
    ),
    ids=("continuous", "categorical", "discrete"))

raster_params = pytest.mark.parametrize(
    "fn, data",
    (
        (raster_cont, continuous_data),
        (raster_discrete, categorical_data),
        (raster_discrete, discrete_data),
    ),
    ids=("continuous", "categorical", "discrete"))

container_params = pytest.mark.parametrize(
    "container",
    (np.asanyarray, list, tuple),
    ids=("array", "list", "tuple"))

@point_params
class TestPoint(object):
    @container_params
    def test_unmasked(self, fn, data, container, coords):
        data = container(data)
        ax = fn(data, coords)
        assert isinstance(ax, plt.Axes)

    def test_masked(self, fn, data, coords, mask):
        masked = np.ma.masked_array(data, mask)
        ax = fn(masked, coords)
        assert isinstance(ax, plt.Axes)

@polygon_params
class TestPolygons(object):
    @container_params
    def test_unmasked(self, fn, data, container, verts):
        data = container(data)
        ax = fn(data, verts)
        assert isinstance(ax, plt.Axes)

    def test_masked(self, fn, data, verts, mask):
        masked = np.ma.masked_array(data, mask)
        ax = fn(masked, verts)
        assert isinstance(ax, plt.Axes)

@raster_params
class TestRaster(object):
    def test_unmasked(self, fn, data):
        raster = to_raster(data)
        ax = fn(raster)
        assert isinstance(ax, plt.Axes)

    def test_masked(self, fn, data, mask):
        masked = np.ma.masked_array(to_raster(data), to_raster(mask))
        ax = fn(masked)
        assert isinstance(ax, plt.Axes)
