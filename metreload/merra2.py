

import os.path
from logzero import logger
from webob.exc import HTTPError

import requests
import xarray as xa
from xarray.backends import PydapDataStore
from pydap.cas.urs import setup_session


DODS_URL = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/dods'

#TODO: Make these command line options
LAT, LON = (47.302765165, 7.100761435)
START_TIME = '1980-01-01'
END_TIME = '1980-01-02'
VARIABLES = ['tlml', 'ulml', 'vlml']

TIME_CHUNKS = {'time': 24}

def get_merra2_data(collection, username, password,
                    savedir,
                    lat=LAT, lon=LON,
                    start_time=START_TIME, end_time=END_TIME,
                    variables=VARIABLES):
    """Convenience function for downloading MERRA-2 data"""
    #TODO: Remove defaults

    with MERRA2Dataset.open(collection, username, password) as dataset:
        dataset.subset(location=(lat, lon),
                       start_time=start_time, end_time=end_time,
                       variables=variables)
        dataset.to_netcdf(savedir)


class MERRA2Dataset(object):
    """Class for MERRA-2 datasets
    """

    def __init__(self, ds):
        """
        Parameters
        ----------
        ds : xarray.Dataset
        """
        self._ds = ds

        # Initially subset equals the whole data
        logger.debug("Making a subset copy")
        self._subset_ds = ds.copy()

        # Get coordinates and variables for this collection
        self._coords = [coord for coord in ds.coords
                        if len(ds.coords[coord]) > 1]
        self._variables = list(ds.data_vars)

    def __del__(self):
        self._subset_ds.close()
        self._ds.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def close(self):
        """Close the dataset"""
        self.__del__()

    @staticmethod
    def open(collection, username, password, base_url=DODS_URL):
        """Open a MERRA-2 data collection

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
        url = '/'.join((base_url, collection.upper()))
        logger.debug("Setting up session to %s as %s", url, username)
        try:
            session = setup_session(username, password, check_url=url)
        except Exception:
            err_str = "Unable to set up session to {} with username {}.".format(url, username)
            raise RuntimeError(err_str)

        logger.debug("Opening Pydap data store")
        try:
            store = PydapDataStore.open(url, session=session)
        except Exception:
            session.close()
            raise RuntimeError("Invalid url '{}'".format(url))

        logger.debug("Opening dataset")
        try:
            dataset = xa.open_dataset(store, chunks=TIME_CHUNKS)
        except HTTPError:
            raise RuntimeError("Authentication failed!")
        finally:
            store.close()
            session.close()

        # Fix for mysterious `area` variable error
        if collection.upper() == 'M2C0NXASM':
            try:
                dataset = dataset.drop('area')
            except KeyError:
                pass

        return MERRA2Dataset(dataset)

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

    def to_xarray(self):
        """Convert to xarray Dataset

        Parameters
        ----------
        squeeze : bool, optional
            If ``True``, drops dimesions with length 1
        """
        logger.debug("Loading dask array to memory")
        return self._subset_ds.squeeze().load()

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
        subset_ds = self._subset_ds

        logger.debug("Subsetting dataset")
        if variables is not None:
            if variables == '*':
                variables_to_get = self._variables
            else:
                variables_to_get = list()
                for var in variables:
                    varname = var.lower()
                    if varname in self._variables:
                        variables_to_get.append(varname)
                    else:
                        logger.warning("Unknown variable '%s'", var)
            if len(variables_to_get) > 0:
                subset_ds = self._ds[variables_to_get]
            else:
                raise RuntimeError("No variables selected")

        # Subset time
        if not (start_time is None and end_time is None):
            if 'time' in self._coords:
                subset_ds = subset_ds.sel(time=slice(start_time, end_time))
            else:
                logger.warning("Trying to time subset a time-invariant collection, ignoring")

        # Subset location
        if location is not None:
            if set(('lat', 'lon')).issubset(self._coords):
                if len(location) == 2:  # TODO: List of points?
                    lat, lon = location
                    assert lat > -90 and lat < 90  # TODO: Better error messages
                    assert lon > -180 and lon < 180
                    kwargs = dict(method='nearest')
                elif len(location) == 4:
                    west, east, south, north = location
                    assert (west <= east and south <= north)  # TODO: better error messages
                    assert all(lon >= -180 and lon <= 180 for lon in (west, east))
                    assert all(lat >= -90 and lat <= 90 for lat in (south, north))
                    lat = slice(south, north)
                    lon = slice(west, east)
                    kwargs = dict()
                else:
                    raise RuntimeError("Wrong number of location arguments.")
            else:
                logger.warning("Trying to location subset a location-invariant collection, ignoring")

            subset_ds = subset_ds.sel(lat=lat, lon=lon, **kwargs)

        self._subset_ds = subset_ds








