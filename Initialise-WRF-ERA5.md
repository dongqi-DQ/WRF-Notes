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

## Step 2: Process with WPS

1. Edit `namelist.wps` to make sure  
  - all datetime stamps match with desired simulation period  
  - all domain sizes are correct

2.  ###geogrid  
  Run `geogrid.exe` (skip this step if `geogrid` has been run before and no domain configuration needs to be changed)
  ```bash
   ./geogrid.exe
  ```

  Outputs should be `geo_em.d0*.nc` containing all geostatic information to run WRF.

3. ###ungrib  
  3.1 link ERA5 girb1 data to WPS directory (recommend to put grib and grib1 files in separate folders)
    ```bash
      ./link_grib.csh path_to_data
    ```
  
  3.2 link [Vtabel.ERA5](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/Vtable.ERA5) so that ungrib can understand ERA5 data
    ```bash
      ln -sf Vtable.ERA5 Vtable
    ```
  
  3.3 run ungrib with `prefix = 'FLIE',` in `namelist.wps`:
    ```bash
     ./ungrib.exe
    ```
      This gives intermediate files like ``FILE:yyyy-mm-dd_HH``.  
      
  3.4 now process uisng [`calc_ecmwf_p.exe`](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/calc_ecmwf_p.exe) for ERA5 initialisation to get intermediate files ``PRES:yyyy-mm-dd_HH``.
  ```bash
     ./calc_ecmwf_p.exe
  ```
4. ###metgrid  
4.1 run `metgrid.exe` with `Prefix='FILE', 'PRES'`
    ```bash
     ./metgrid.exe
    ```
    
   Outputs files: `met_em.d0*.yyyy-mm-dd_HH:MM:SS.nc`

## Step 3: Run WRF
1. link met_em files to `WRF/run` directory
    ```bash
     ln -sf ../WPS/met_em.d0* .
    ```
2. run real.exe and then if no error occurred, run wrf.exe
