"""Test pydap connections"""

import xarray as xa

def test_pydap():
    url = 'http://test.opendap.org/opendap/hyrax/data/nc/bears.nc'
    with xa.open_dataset(url, engine='pydap') as ds:
        pass
