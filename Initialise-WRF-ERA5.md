# A simple walkthrough to initialise WRF with ERA5

For further details please refer to [this article](https://dreambooker.site/2018/04/20/Initializing-the-WRF-model-with-ERA5/) by Xin Zhang.

## Step 1: Download data

1. Use [`dl.py`](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/dl.py) script to downlaod ERA5 data.  
  - Define start and end datetime stamp in the following lines:
  
  ```python
  start_year = 2017
  end_year = 2017
  dates = np.arange(datetime(2017, 2, 10), datetime(2017, 2, 18), timedelta(days=1)).astype(datetime)
  ```
  
  - To make download faster and easier, make sure the correct downlaod area is chosen (format in latitudes/longitudes: north/west/south/east):
  ```python
  'area': '-20/145/-65/-160',
  ```
  
  The area here is for New Zealand domain/  
  This will download two grib files for each day including 3-hourly ERA5 data `ERA5_yyyymmdd-ml.grib` and `ERA5_yyyymmdd-sfc.grib`. 
  
2. Process ERA5 raw data using [`process.sh`](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/process.sh).
   ```bash
   ./process.sh
   ```
   
   This should give two grib1 files for each day `ecmf_yyyymmdd_an_ml_0.grib1` and `ecmf_yyyymmdd_an_sfc_0.grib1`. 
   
**Tips:** if you wish to preview the files, [panoply](https://www.giss.nasa.gov/tools/panoply/) is a quite handy tool.

