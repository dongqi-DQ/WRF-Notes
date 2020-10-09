# Initialise WRF with GFS forecast

This is relatively easier than using ERA5.

## Step 1 Download data

### 1.1 GFS grib2 data

UC ethernet is having trouble logging onto NCAR/UCAR research data archive. We either cannot create a new account or sign in. Since we will download multiple files anyway, it is necessary to have a script to download data automatically.

So I found this page helpful for downloading data: https://metclim.ucd.ie/2017/04/download-gfs-forecast/

NOAA has a NOMADS system where all data sets can be found: https://nomads.ncep.noaa.gov/

Now select **`grib filter`** for GFS data set (in my case **`GFS 0.25 Degree`**). Then you will see a list of subdirectory. Choose the date (`gfs.YYYYMMDD`) you want to start your forecast with and the start hour (in UTC). 

Next step is to select forecast data rather than analysis. In the file drop down menu, select data end with `f000` for forecast starts from 0000 UTC of the date you chosen before. Then choose all levels and all variables. 

To save disk space and time for data downloading, choose `make subregion` in `Extract Subregion`. Here logitude can be from 0 to 360 and latitude can be from 90 to -90. For New Zealand case, I put 
```
left longitude = 145     right longitude = 200
top latitude   = -20     bottom latitude = -65
```

Note that here you cannot use negative numbers for right longitude if left longitude is positive. Otherwise, you will only get empty files. 

Now select `Show the URL`. You will get a URL like:  
https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t00z.pgrb2.0p25.f000URL2='&all_lev=on&all_var=on&subregion=&leftlon=140&rightlon=200&toplat=-20&bottomlat=-65&dir=%2Fgfs.20200929%2F00


This URL contains different parts:

- **file=gfs.t00z.pgrb2.0p25.f000** – this is the base file name: model GFS, forecast initial time 00Z, grb2 format, forecast hour is 000. The forecast hour is what we want to change.
- **dir=%2Fgfs.20200929%2F00** – this is the year, month, day and hour of the forecast initial time. All forecast data are inside this directory.
- We don’t want to change the rest of the URL: forecast model, level, variables, subregion. If you want to change these, go through the grib_filter web page again and get a new URL.

If we want to download multiple forecast hours for the same forecast initial time, we could do so with a bash script like this:

```
#!/bin/bash

# set the base URL in two parts: URL1 and URL2
# leave our forecast hour:

DATE = '20200929'
URL1='http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?file=gfs.t00z.pgrb2.0p25.f'

URL2='&lev_surface=on&var_TMP=on&subregion=&leftlon=-7&rightlon=-5&toplat=54&bottomlat=52&dir=%2Fgfs.'${DATE}'%F00'

# Let forecast hour vary from 0 to 24.
# It needs to have three digits, so we start with 1000:

for i in {0..24}
do
  echo $i
  TFCH=`expr 1000 + $i`
  FCH=`echo $TFCH | cut -c2-4`
  URL=${URL1}${FCH}${URL2}
  curl $URL -o GFS_$DATE_${FCH}.grb
done
```

Save this bash script as `getGFS.bash` and run. You will get information like:
```
0
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 27.7M    0 27.7M    0     0  1245k      0 --:--:--  0:00:22 --:--:-- 1418k
```

Note that if you get files that are empty or very small (~400 K), you might have done something wrong when setting up the subregion. Go back to the grib_filter web and check the longitudes and latitudes are correct.


### 1.2 Static Data
Static Data are available from [WRF User page](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)

The high resolution one is currently the optimal one for New Zealand domain. We only need the mandatory domain for simple forecast. Download the file `geog_high_res_mandatory.tar.gz` and unzip it:  
```
tar xvzf geog_high_res_mandatory.tar.gz
```


## Step 2: WPS
Now we have all the data to run WPS and then WRF. 
### 2.1 specify run date and domains
<WRF domain wizard?>


Edit namelist.wps to make sure  
- all datetime stamps match with desired simulation period  
- all domain sizes are correct  

### 2.2 Run geogrid
Run `geogrid.exe` (skip this step if `geogrid` has been run before and no domain configuration needs to be changed)  
  ```
   ./geogrid.exe
  ```

  Outputs should be `geo_em.d0*.nc` containing all geostatic information to run WRF.
### 2.3 Run Ungrib

1. link GFS grib2 data to WPS directory
    ```
      ./link_grib.csh path_to_data/files
    ```
  
2. link Vtabel.ARW so that ungrib can understand GFS data  
    ```
      ln -sf Vtable.GFS Vtable
    ```
  
3. run ungrib with `prefix = 'FLIE',` in `namelist.wps`:    
    ```
     ./ungrib/ungrib.exe
    ```
      This gives intermediate files like ``FILE:yyyy-mm-dd_HH``.  

4. link `Vtable.SST` for SST from GFS:
 ```
      ln -sf Vtable.SST Vtable
   ```
5. run ungrib with `prefix = 'SST',` in `namelist.wps`:    
    ```
     ./ungrib/ungrib.exe
    ```
      This gives intermediate files like ``SST:yyyy-mm-dd_HH``.  


### 2.4: Run Metgrid

1. link to the correct `METGRID.TBL`:
  ```
  ln -sf METGRID.TBL.ARW METGRID.TBL
  ```

2. run `metgrid.exe` with `Prefix='FILE', 'PRES'` in `namelist.wps`  
    ```
     ./metgrid/metgrid.exe
    ```
Outputs files: `met_em.d0*.yyyy-mm-dd_HH:MM:SS.nc`

## Step 3: Run WRF

Go to WRF directory:
```
cd ../WRF/run
```
link all `met_em` files to run directory:
```
ln -sf ../WPS/met_em.d0* .
```

edit `namelist.input` and run `real.exe`

check `rsl.error.0000` to make sure no error occured:
```
d01 2020-09-30_00:00:00 real_em: SUCCESS COMPLETE REAL_EM INIT
```

Then run WRF with MPI: 
```
time mpirun -np 8 ./wrf.exe &
```

Use `tail` to check run status:
```
tail -f rsl.error.0000
```

