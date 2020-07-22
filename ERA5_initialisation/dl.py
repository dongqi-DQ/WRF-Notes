import cdsapi

import numpy as np
from datetime import datetime, timedelta
import os


start_year = 2017
end_year = 2017
dates = np.arange(datetime(2017, 2, 10), datetime(2017, 2, 18), timedelta(days=1)).astype(datetime)
#dates_2 = np.arange(datetime(2019, 8, 1), datetime(2019, 8, 30), timedelta(days=1)).astype(datetime)
#dates = np.append(dates, dates_2)
print(dates)


def raw_date(dt):
    return dt.strftime("%Y%m%d")


def get_3d_var(dt, out_fname):
    c = cdsapi.Client()
    c.retrieve('reanalysis-era5-complete', {
            'class': 'ea',
            'date': f'{raw_date(dt)}/to/{raw_date(dt)}',
            'area': '-20/145/-65/-160',
            'expver': '1',
            'levelist': '1/to/137',
            'levtype': 'ml',
            'param': '129/130/131/132/133/152',
            'stream': 'oper',
            'time': '00:00:00/03:00:00/06:00:00/09:00:00/12:00:00/15:00:00/18:00:00/21:00:00',
            'type': 'an',
            'grid': "0.25/0.25",
        }, out_fname)


def get_d2_var(dt, out_fname):
    c = cdsapi.Client()
    c.retrieve('reanalysis-era5-complete', {
        'class': 'ea',
        'date': f'{raw_date(dt)}/to/{raw_date(dt)}',
        'area': '-20/145/-65/-160',
        'expver': '1',
        'levtype': 'sfc',
        'param': 'msl/sp/skt/2t/10u/10v/2d/z/lsm/sst/ci/sd/stl1/stl2/stl3/stl4/swvl1/swvl2/swvl3/swvl4',
        'stream': 'oper',
        'time': '00:00:00/03:00:00/06:00:00/09:00:00/12:00:00/15:00:00/18:00:00/21:00:00',
        'type': 'an',
        'grid': "0.25/0.25",
    }, out_fname)


# if not os.path.exists(out_folder):
#     os.makedirs(out_folder, exist_ok=True)

for dt in dates:
    for lvl_type in ['sfc', 'ml']:

        out_fname = 'ERA5_{}-{}.grib'.format(raw_date(dt), lvl_type)
        if not os.path.exists(out_fname):
            if lvl_type == 'sfc':
                get_d2_var(dt, out_fname)
            else:
                get_3d_var(dt, out_fname)
        else:
            print('Skipping ' + out_fname + ' as it already exists')
