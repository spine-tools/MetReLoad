"""Test MERRA-2 functionality"""

import pytest

from metreload.merra2 import get_merra2_data

@pytest.mark.filterwarnings("ignore:password was not set")
def test_merra2_session(tmpdir):
    with pytest.raises(RuntimeError):
        get_merra2_data(collection='M2C0NXASM', 
                        username=None, 
                        password=None, 
                        lat=None, lon=None, 
                        start_time=None, end_time=None,
                        out_dir=tmpdir)

@pytest.mark.filterwarnings("ignore:password was not set")
def test_merra2_collection(tmpdir):
    with pytest.raises(RuntimeError):
        get_merra2_data(collection='foobar', 
                        username=None, 
                        password=None, 
                        lat=None, lon=None, 
                        start_time=None, end_time=None,
                        out_dir=tmpdir)