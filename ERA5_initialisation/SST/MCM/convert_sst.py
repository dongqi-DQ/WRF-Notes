#!/usr/bin/env python
# coding: utf-8


'''
Python script to convert netcdf SST (CMC) to WPS intermediate file
and interpolate in time


Input from user:
- file path (all netcdf should be in the same folder)
- output path
- start date
- end date
- update interval (for interpolation)
- south-west corner latitude and longitude of the SST data set
- latitude and longitude increment

More details see pywinter documentation
'''



import xarray as xr
import numpy as np
import pywinter.winter as pyw
import pandas as pd
from glob import glob
import os



sst_path = '/data/WRF-model/DATA/CMC_SST/2019/'
path_out = '/data/WRF-model/V4.2/WPS-4.2/'
start_date = '20190724' # YYYYMMDD
end_date = '20190727'   # YYYYMMDD
interval = '1H'         # update interval
llc_lat = -90            # south-west corner latitude
llc_lon = 0             # south-west corner longitude
dlat = 0.1             # latitude increment (degrees)
dlon = 0.1              # longitude increment (degrees)
all_days = pd.date_range(start=start_date, end=end_date, freq='D')
all_days = [str(day)[:10] for day in all_days]



sst_files = sorted(glob(sst_path+'*.nc'))



ds_sst = xr.open_mfdataset(sst_files)



sst_days = ds_sst.sel(time=slice(start_date, end_date)).chunk({'time':-1,'lat':-1, 'lon':-1})



ds_sst_interp = sst_days.interp(time=pd.date_range(start_date, end_date, freq=interval))
# convert dimensions
sst_raw = ds_sst_interp['analysed_sst'][:,:,:]
lat_raw = ds_sst_interp['lat']
lon_raw = ds_sst_interp['lon']
lon_new = np.zeros(lon_raw.shape[0])
lat_new = np.zeros(lat_raw.shape[0])
sst_new = np.zeros((sst_raw.shape[0], sst_raw.shape[1], sst_raw.shape[2]))
lat_new[:] = lat_raw.data[:]
lon_new[0:int(len(lon_new)/2)] = lon_raw[int(len(lon_new)/2):]
lon_new[int(len(lon_new)/2):] = lon_raw[0:int(len(lon_new)/2)] + 360
sst_new[:,:, 0:int(len(lon_new)/2)] = sst_raw[:,:, int(len(lon_new)/2):]
sst_new[:,:, int(len(lon_new)/2):] = sst_raw[:,:, 0:int(len(lon_new)/2)]


for idx, ts in enumerate(ds_sst_interp.time.data):
    date = str(ts)[:10]
    hour = str(ts)[11:13]
    # geo-information
    winter_geo = pyw.Geo0(llc_lat, llc_lon, dlat, dlon)
    # must use level = '200100', otherwise metgrid will crash
    winter_sst = pyw.V2d('SST', sst_new[idx,:,:], 'Sea surface temperature','K','200100') 
    pyw.cinter('SST',date+'_'+hour, winter_geo, [winter_sst], path_out)



