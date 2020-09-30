# Initialise WRF with GFS forecast

This is relatively easier than using ERA5.

## Step 1 Download GFS grib2 data

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

**!!I copied everything below. Will rewrite later!!**

This code contains different parts:

- file=gfs.t12z.pgrb2.0p25.f000 – this is the base file name: model GFS, forecast initial time 12Z, …, forecast hour is 000. The forecast hour is probably what we want to change.
- dir=%2Fgfs.2017041712 – this is the year, month, day and hour of the forecast initial time. All forecast data are inside this directory.
- We don’t want to change the rest of the URL: forecast model, level, variables, subregion. If you want to change these, go through the grib_filter web page again and generate a new URL.

If we want to download multiple forecast hours for the same forecast initial time, we could do so with a bash script like this:

```
#!/bin/bash

# set the base URL in two parts: URL1 and URL2
# leave our forecast hour:

URL1='http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?file=gfs.t12z.pgrb2.0p25.f'

URL2='&lev_surface=on&var_TMP=on&subregion=&leftlon=-7&rightlon=-5&toplat=54&bottomlat=52&dir=%2Fgfs.2017041712'

# Let forecast hour vary from 0 to 24.
# It needs to have three digits, so we start with 1000:

for i in {0..24}
do
  echo $i
  TFCH=`expr 1000 + $i`
  FCH=`echo $TFCH | cut -c2-4`
  URL=${URL1}${FCH}${URL2}
  curl $URL -o GFS${FCH}.grb
done
```


## Step 2: SST data
<optional?>  

NCEP SST was discontinued on Feb. 11, 2020. Here is a forum talking about replacements: https://github.com/wrf-model/WRF/issues/1159

A good replacement we found is NASA JPL SST (Sea Surface Temperature) dataset, whic is available from  June 1st, 2002 to the present. UC team already has a (kinda) [technical documentation](https://wiki.canterbury.ac.nz/display/UCHPC/Using+MUR+SST+data+to+nudge+WRF+simulations) for using NASA SST to run WRF. I will replicate the process and write something here.  



The following Drive API Credentials should be used when developing scripts to access or download files from the PO.DAAC Drive API.

The Drive API password is different than your Earthdata Login password.

Click the '?' for the FAQ to see examples of scripted API access, which include your Drive-specific login credentials.
Your PO.DAAC Drive API Credentials (WebDAV)

```
Install required software

Install davfs2 package to mount WebDAV resource as regular file system.

$ sudo apt-get install davfs2

Mount WebDAV share using command-line

Create the mountpoint directory.

$ sudo mkdir /mnt/dav

```

## Step 3: Run WPS

This is easier than ERA5. Not too much preprocessing needed.
