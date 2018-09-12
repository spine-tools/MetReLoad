

import os.path
from logzero import logger
from webob.exc import HTTPError

import requests
import xarray as xa
from xarray.backends import PydapDataStore
from pydap.cas.urs import setup_session

DODS_URL = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/dods'

def get_merra2_data(collection, username, password,
                    savedir,start_time, end_time,variables,
                    location):
    """Convenience function for downloading MERRA-2 data"""
    with MERRA2Dataset(collection, username, password) as dataset:
        dataset.subset(location,
                       start_time=start_time, end_time=end_time,
                       variables=variables)
        dataset.to_netcdf(savedir)


class MERRA2Dataset(object):
    """Class for MERRA-2 datasets
    """

    def __init__(self, collection, username, password,
                 base_url=DODS_URL):
        """
        Parameters
        ----------
        collection : str
            Earth Science Data Types Name of the collection (9 characters)
        username : str
        password : str
            Password
        base_url : str, optional
            Base url for requests, default https://goldsmr4.gesdisc.eosdis.nasa.gov/dods
        """

        # Initialize with empty data
        self._ds = xa.Dataset()
        self._subset_ds = self._ds
        self._session = requests.Session()
        self._store = PydapDataStore(xa.Dataset())

        # Initialize session and open dataset
        url = '/'.join((base_url, collection))
        logger.debug("Setting up session to %s as %s", url, username)
        try:
            self._session = setup_session(username, password, check_url=url)
        except Exception:
            err_str = "Unable to set up session to {} with username {}.".format(url, username)
            raise RuntimeError(err_str)

        logger.debug("Opening Pydap data store")
        try:
            self._store = PydapDataStore.open(url, session=self._session)
        except Exception:
            raise RuntimeError("Invalid url {}".format(url))
        finally:
            self._session.close()

        logger.debug("Opening dataset")
        try:
            self._ds = xa.open_dataset(self._store, chunks={'time': 24})
        except HTTPError:
            raise RuntimeError("Authentication failed!")
        finally:
            self._store.close()
            self._session.close()

        # Initially subset equals the whole data
        self._subset_ds = self._ds

    def __del__(self):
        self._subset_ds = None
        self._ds = None
        self._store.close()
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def to_netcdf(self, savedir):
        """Save to netCDF4 files

        Parameters
        ----------
        savedir : str
            Path to save files to
        freq : str, optional
            Pandas frquency string, default 1 day ('D')
            (see https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases)
        """

        # Add dates
        self._subset_ds['date'] = self._subset_ds.time.to_pandas().dt.strftime('%Y%m%d')

        # Write as multi-file dataset
        dates, datasets = zip(*self._subset_ds.groupby('date'))
        basename = self._ds.attrs['title'].split(':')[0].replace(' ', '.')
        filepaths = [os.path.abspath(os.path.join(savedir,
                                     '{}.{}.SUB.nc4'.format(basename, date)))
                    for date in dates]
        logger.debug("Writing to %s", os.path.abspath(savedir))
        xa.save_mfdataset(datasets, filepaths)

    def to_xarray(self, squeeze=True):
        """Convert to xarray Dataset

        Parameters
        ----------
        squeeze : bool, optional
            If ``True``, drops dimesions with length 1
        """

        if squeeze:
            return self._subset_ds.squeeze(drop=True)
        else:
            return self._subset_ds

    def subset(self, location=None, 
               start_time=None, end_time=None,
               variables=None):
        """Subset the data accordingly

        Parameters
        ----------
        location : tuple
            Location in the form of tuple (lat, lon) or (west, east, south, north)
            coordinates in WGS84 system.
        start_time : str
            Timestamp in the form YYYY-MM-DDTHH
        end_time : str
            See above.
        variables : list
            List of variables to include, or '*' to include all
        """
        logger.debug("Subsetting dataset")
        if variables is not None:
            if variables == '*':
                variables = list(self._ds.data_vars.keys())
            subset_ds = self._ds[variables]        

        # Subset time
        if not (start_time is None and end_time is None):
            subset_ds = subset_ds.sel(time=slice(start_time, end_time))

        # Subset location
        if location is None:
            raise RuntimeError("Wrong number of location arguments.")
        elif len(location)==2:
            lat, lon = location 
        elif len(location)==4:
            north, west, south, east = location
            lat = [south, north]
            lon = [west, east]            
        else:
            raise RuntimeError("Wrong number of location arguments.")
        
        print("lat",lat,"\nlon",lon)
        subset_ds = subset_ds.sel(lat=lat, lon=lon, 
                                      method='nearest', drop=True)
        self._subset_ds = subset_ds








