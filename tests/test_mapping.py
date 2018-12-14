from collections import OrderedDict
import pytest
import numpy as np

from fieldmaps import mapping


categorical_data = np.array(["a", "a", "b", "b", "c", "c"])
categorical_data.setflags(write=False)

discrete_data = np.array([-1, -1, 3, 3, 99, 99])
discrete_data.setflags(write=False)

@pytest.fixture(scope="module")
def mask():
    data = np.array([True, True, False, False, False, False])
    data.setflags(write=False)
    return data

@pytest.mark.parametrize("test_input,expected_keys,expected_values", [
    (categorical_data, ("a", "b", "c"), (0, 1, 2)),
    (discrete_data, (-1, 3, 99), (0, 1, 2)),
])
def test_mk_internal_map(test_input, expected_keys, expected_values):
    # One-dim array.
    out = mapping.mk_internal_map(test_input)

    assert isinstance(out, OrderedDict)
    assert tuple(out.keys()) == expected_keys
    assert tuple(out.values()) == expected_values

    # Two-dim array.
    new_shape = (int(len(test_input) / 2), 2)
    raster = np.reshape(test_input, new_shape)
    out = mapping.mk_internal_map(raster)

    assert tuple(out.keys()) == expected_keys
    assert tuple(out.values()) == expected_values

def test_internal_array():
    pairs = {"a": 1, "b": 2, "c": 3}
    data = np.array(["a", "b", "b", "c", "d"])
    expected = np.array([1, 2, 2, 3, mapping._fill])

    out = mapping.internal_array(data, pairs)

    assert out.dtype == mapping._dtype
    assert np.all(out == expected)

@pytest.mark.parametrize("test_input", [
    categorical_data,
    discrete_data,
])
def test_create_mapped(test_input, mask):
    # Unmasked input.
    expected = np.array([0, 0, 1, 1, 2, 2])
    pairs, mock = mapping.create_mapped(test_input)

    assert isinstance(mock, np.ma.MaskedArray)
    assert mock.shape == test_input.shape
    assert np.all(mock == expected)
    assert not np.any(mock.mask)
    assert len(pairs) == 3

    # Masked input.
    masked_input = np.ma.masked_array(test_input, mask)
    expected_masked = np.ma.masked_array(
        [mapping._fill, mapping._fill, 0, 0, 1, 1],
        mask)
    pairs, mock = mapping.create_mapped(masked_input)

    assert isinstance(mock, np.ma.MaskedArray)
    assert mock.shape == masked_input.shape
    assert np.all(mock == expected_masked)
    assert np.all(mock.mask == mask)
    assert len(pairs) == 2

def test_discrete_norm():
    data = (0, 1, 2)
    norm = mapping.discrete_norm(data)

    assert norm.vmin == 0
    assert norm.vmax == 3
    assert norm.N == len(data) + 1
    assert list(norm.boundaries) == [0, 1, 2, 3]

def test_discrete_cmap():
    data = np.array([0, 1, 2])
    cmap = mapping.discrete_cmap(data, "tab10")

    assert cmap.N == len(data)
    assert cmap.colors.shape == (len(data), 4)

def test_add_discrete_labels():
    class MockColorbar(object):
        def set_ticks(self, ticks):
            self.ticks = ticks

        def set_ticklabels(self, ticklabels):
            self.ticklabels = ticklabels

    labels = (0, 1, 2)
    cbar = MockColorbar()
    out = mapping.add_discrete_labels(cbar, labels)

    assert out is cbar
    assert np.all(out.ticks == np.array([.5, 1.5, 2.5]))
    assert out.ticklabels == labels
