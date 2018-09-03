

import os.path
from logzero import logger
from webob.exc import HTTPError

import xarray as xa
from pydap.cas.urs import setup_session


BASE_URL = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/dods'

#TODO: Make these command line options
LAT, LON = (47.302765165, 7.100761435)
START_TIME = '1980-01-01'
END_TIME = '1980-01-02'
VARIABLES = ['tlml', 'ulml', 'vlml']

def get_merra2_data(collection, username, password, 
                    out_dir,
                    lat=LAT, lon=LON, 
                    start_time=START_TIME, end_time=END_TIME,
                    variables=VARIABLES):

    # Construct the URL
    url = '/'.join((BASE_URL, collection))

    logger.debug("Setting up session to %s as %s", url, username)
    with setup_session(username=username, password=password,
                       check_url=url) as session:
        logger.debug("Opening Pydap data store")
        try:
            store = xa.backends.PydapDataStore.open(url, session=session)
        except Exception:
            raise RuntimeError("Invalid collection name")

        logger.debug("Opening dataset")
        try:
            src_ds = xa.open_dataset(store, chunks={'time': 24})
        except HTTPError:
            raise RuntimeError("Authentication failed!")

        subset_ds = (src_ds[variables].sel(time=slice(start_time, end_time))
                                    .sel(lat=lat, lon=lon, method='nearest',
                                        drop=True))
        # Add dates
        subset_ds['date'] = subset_ds.time.to_pandas().dt.strftime('%Y%m%d')

        # Write as multi-file dataset
        dates, datasets = zip(*subset_ds.groupby('date'))
        basename = src_ds.attrs['title'].split(':')[0].replace(' ', '.')
        filepaths = [os.path.join(out_dir, 
                                '{}.{}.SUB.nc4'.format(basename, date))
                    for date in dates]
        xa.save_mfdataset(datasets, filepaths)
