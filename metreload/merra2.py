

import os.path
from logzero import logger

import pandas as pd
import xarray as xa
from pydap.cas.urs import setup_session


BASE_URL = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/dods'

def get_merra2_data(collection, user, password, out_dir):

    # Construct the URL
    url = '/'.join((BASE_URL, collection))

    LOCATIONS = {'loc1': (47.302765165, 7.100761435),
    #             'loc2': (65.25628568,	17.28856116),
    #             'loc3': (60.34302959130653, 13.948979161811456),
    #             'loc4':  (63.09723221389482, 17.151276444868675)
                }

    START_TIME = '1980-01-01'
    END_TIME = '1980-01-02'

    VARIABLES = ['tlml', 'ulml', 'vlml']

    logger.debug("Setting up session to %s", url)
    session = setup_session(username=user, password=password,
                            check_url=url)
    store = xa.backends.PydapDataStore.open(url, session=session)

    logger.debug("Opening dataset")
    src = xa.open_dataset(store, chunks={'time': 24})

    data = src[VARIABLES].sel(time=slice(START_TIME, END_TIME))

    out = xa.Dataset(coords={'time': data['time'],
                            'location': list(LOCATIONS.keys())})

    datasets = list()
    for loc, (x, y) in LOCATIONS.items():
        datasets.append(data.sel(lat=y, lon=x, method='nearest', drop=True))
    out = xa.concat(datasets, dim=pd.Index(LOCATIONS.keys(), name='location'))
    out['date'] = out.time.to_pandas().dt.strftime('%Y%m%d')

    dates, datasets = zip(*out.groupby('date'))

    basename = out.attrs['title'].split(':')[0].replace(' ', '.')
    filepaths = [os.path.join(out_dir, 
                            '{}.{}.SUB.nc4'.format(basename, date)) 
                for date in dates]

    xa.save_mfdataset(datasets, filepaths)
