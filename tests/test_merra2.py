"""Test MERRA-2 functionality"""

import pytest

from metreload.merra2 import MERRA2Dataset

@pytest.mark.filterwarnings("ignore:password was not set")
def test_merra2_session():
    with pytest.raises(RuntimeError):
        with MERRA2Dataset('M2C0NXASM', username=None, password=None) as dataset:
            pass


@pytest.mark.filterwarnings("ignore:password was not set")
def test_merra2_collection():
    with pytest.raises(RuntimeError):
        with MERRA2Dataset('foobar', username=None, password=None) as dataset:
            pass
            