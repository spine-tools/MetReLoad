"""Test MERRA-2 functionality"""
# pylint: disable=missing-docstring,redefined-outer-name

import os.path
import pytest
from xarray import open_dataset
import pandas as pd

from metreload.merra2 import MERRA2Dataset


def get_dataset(directory, collection_name):
    filepath = os.path.join(directory, '{}.nc'.format(collection_name))
    return open_dataset(filepath)


@pytest.fixture
def time_invariant_dataset(shared_datadir):
    with get_dataset(shared_datadir, 'M2C0NXASM') as src,\
         MERRA2Dataset(src) as dataset:
        yield dataset


@pytest.fixture
def time_variant_dataset(shared_datadir):
    with get_dataset(shared_datadir, 'M2I1NXASM') as src:
        with MERRA2Dataset(src) as dataset:
            yield dataset


@pytest.mark.filterwarnings("ignore:password was not set")
def test_merra2_session():
    with pytest.raises(RuntimeError):
        MERRA2Dataset.open('M2C0NXASM', username=None, password=None)


@pytest.mark.filterwarnings("ignore:password was not set")
def test_merra2_collection():
    with pytest.raises(RuntimeError):
        MERRA2Dataset.open('foobar', username=None, password=None)


def test_time_invariant_collection(time_invariant_dataset):
    time_invariant_dataset.subset(location=(0, 0))
    ds = time_invariant_dataset.to_xarray()
    with pytest.raises(TypeError):
        len(ds['time'])


@pytest.mark.filterwarnings("ignore:password was not set")
def test_merra2_collection_to_dataframe(time_variant_dataset):
    assert isinstance(time_variant_dataset.to_dataframe(), pd.DataFrame)
