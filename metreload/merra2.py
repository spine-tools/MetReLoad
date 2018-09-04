

import os.path
from logzero import logger
from webob.exc import HTTPError

import xarray as xa
from xarray.backends import PydapDataStore
from pydap.cas.urs import setup_session


DODS_URL = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/dods'

#TODO: Make these command line options
LAT, LON = (47.302765165, 7.100761435)
START_TIME = '1980-01-01'
END_TIME = '1980-01-02'
VARIABLES = ['tlml', 'ulml', 'vlml']

def get_merra2_data(collection, username, password,
                    savedir,
                    lat=LAT, lon=LON,
                    start_time=START_TIME, end_time=END_TIME,
                    variables=VARIABLES):
    """Convenience function for downloading MERRA-2 data"""
    #TODO: Remove defaults

    with MERRA2Dataset(collection, username, password) as dataset:
        dataset.subset(location=(lat, lon),
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
        if location is not None:
            if len(location) == 2:  # TODO: List of points?
                lat, lon = location
                assert lat > -90 and lat < 90  # TODO: Better error messages
                assert lon > -180 and lon < 180
            elif len(location) == 4:
                west, east, south, north = location
                assert (west < east and south < north)  # TODO: better error messages
                assert all(lon > -180 and lon < 180 for lon in (west, east))
                assert all(lat > -90 and lat < 90 for lat in (south, north))
                lat = slice(south, north)
                lon = slice(west, east)
            else:
                raise RuntimeError("Wrong number of location arguments.")

            subset_ds = subset_ds.sel(lat=lat, lon=lon, 
                                      method='nearest', drop=True)

        self._subset_ds = subset_ds








