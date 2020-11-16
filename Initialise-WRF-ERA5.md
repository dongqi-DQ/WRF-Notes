# A simple walkthrough to initialise WRF with ERA5

For further details please refer to [this article](https://dreambooker.site/2018/04/20/Initializing-the-WRF-model-with-ERA5/) by Xin Zhang.

## Step 1: Download data

1. Use [`dl.py`](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/dl.py) script to downlaod ERA5 data.  
  - Specify start and end datetime stamp in the following lines:
  
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
   ```
     ./process.sh
   ```
   
   This should give two grib1 files for each day `ecmf_yyyymmdd_an_ml_0.grib1` and `ecmf_yyyymmdd_an_sfc_0.grib1`. 
**Note:** to use `grib_filter` and `grib_set`, use Anaconda to install ecmwf_grib     
  ```
   conda install -c conda-forge ecmwf_grib 
  ```
**Tips:** if you wish to preview the grib files, [panoply](https://www.giss.nasa.gov/tools/panoply/) is a quite handy tool.  

3. Static Data are available from [WRF User page](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)

## Step 2: Process with WPS

1. Edit `namelist.wps` to make sure  
  - all datetime stamps match with desired simulation period  
  - all domain sizes are correct

2.  **geogrid**  
  Run `geogrid.exe` (skip this step if `geogrid` has been run before and no domain configuration needs to be changed)  
  ```
   ./geogrid.exe
  ```

  Outputs should be `geo_em.d0*.nc` containing all geostatic information to run WRF.

3. **ungrib**  
  3.1 link ERA5 girb1 data to WPS directory (recommend to put grib and grib1 files in separate folders)  
    ```
      ./link_grib.csh path_to_data/files
    ```
  
  3.2 link [Vtabel.ERA5](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/Vtable.ERA5) so that ungrib can understand ERA5 data  
    ```
      ln -sf Vtable.ERA5 Vtable
    ```
  
  3.3 run ungrib with `prefix = 'FLIE',` in `namelist.wps`:    
    ```
     ./ungrib/ungrib.exe
    ```
      This gives intermediate files like ``FILE:yyyy-mm-dd_HH``.  
      
  3.4 now process uisng [`calc_ecmwf_p.exe`](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/calc_ecmwf_p.exe) for ERA5 initialisation to get intermediate files ``PRES:yyyy-mm-dd_HH``. This requires a ecmwf coeff table [`ecmwf_coeff`](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/ecmwf_coeffs)  
   **Note: Do NOT run ungrib for PRES files!!**
  ```
  0 0.000000 0.00000000  
1 2.000365 0.00000000  
2 3.102241 0.00000000  
3 4.666084 0.00000000  
4 6.827977 0.00000000  
5 9.746966 0.00000000  
6 13.605424 0.00000000  
7 18.608931 0.00000000  
8 24.985718 0.00000000  
9 32.985710 0.00000000  
10 42.879242 0.00000000  
11 54.955463 0.00000000  
12 69.520576 0.00000000  
13 86.895882 0.00000000  
14 107.415741 0.00000000  
15 131.425507 0.00000000  
16 159.279404 0.00000000  
17 191.338562 0.00000000  
18 227.968948 0.00000000  
19 269.539581 0.00000000  
20 316.420746 0.00000000  
21 368.982361 0.00000000  
22 427.592499 0.00000000  
23 492.616028 0.00000000  
24 564.413452 0.00000000  
25 643.339905 0.00000000  
26 729.744141 0.00000000  
27 823.967834 0.00000000  
28 926.344910 0.00000000  
29 1037.201172 0.00000000  
30 1156.853638 0.00000000  
31 1285.610352 0.00000000  
32 1423.770142 0.00000000  
33 1571.622925 0.00000000  
34 1729.448975 0.00000000  
35 1897.519287 0.00000000  
36 2076.095947 0.00000000  
37 2265.431641 0.00000000  
38 2465.770508 0.00000000  
39 2677.348145 0.00000000  
40 2900.391357 0.00000000  
41 3135.119385 0.00000000  
42 3381.743652 0.00000000  
43 3640.468262 0.00000000  
44 3911.490479 0.00000000  
45 4194.930664 0.00000000  
46 4490.817383 0.00000000  
47 4799.149414 0.00000000  
48 5119.895020 0.00000000  
49 5452.990723 0.00000000  
50 5798.344727 0.00000000  
51 6156.074219 0.00000000  
52 6526.946777 0.00000000  
53 6911.870605 0.00000000  
54 7311.869141 0.00000000  
55 7727.412109 0.00000700  
56 8159.354004 0.00002400  
57 8608.525391 0.00005900  
58 9076.400391 0.00011200  
59 9562.682617 0.00019900  
60 10065.978516 0.00034000  
61 10584.631836 0.00056200  
62 11116.662109 0.00089000  
63 11660.067383 0.00135300  
64 12211.547852 0.00199200  
65 12766.873047 0.00285700  
66 13324.668945 0.00397100  
67 13881.331055 0.00537800  
68 14432.139648 0.00713300  
69 14975.615234 0.00926100  
70 15508.256836 0.01180600  
71 16026.115234 0.01481600  
72 16527.322266 0.01831800  
73 17008.789062 0.02235500  
74 17467.613281 0.02696400  
75 17901.621094 0.03217600  
76 18308.433594 0.03802600  
77 18685.718750 0.04454800  
78 19031.289062 0.05177300  
79 19343.511719 0.05972800  
80 19620.042969 0.06844800  
81 19859.390625 0.07795800  
82 20059.931641 0.08828600  
83 20219.664062 0.09946200  
84 20337.863281 0.11150500  
85 20412.308594 0.12444800  
86 20442.078125 0.13831300  
87 20425.718750 0.15312500  
88 20361.816406 0.16891000  
89 20249.511719 0.18568900  
90 20087.085938 0.20349100  
91 19874.025391 0.22233300  
92 19608.572266 0.24224400  
93 19290.226562 0.26324200  
94 18917.460938 0.28535400  
95 18489.707031 0.30859800  
96 18006.925781 0.33293900  
97 17471.839844 0.35825400  
98 16888.687500 0.38436300  
99 16262.046875 0.41112500  
100 15596.695312 0.43839100  
101 14898.453125 0.46600300  
102 14173.324219 0.49380000  
103 13427.769531 0.52161900  
104 12668.257812 0.54930100  
105 11901.339844 0.57669200  
106 11133.304688 0.60364800  
107 10370.175781 0.63003600  
108 9617.515625 0.65573600  
109 8880.453125 0.68064300  
110 8163.375000 0.70466900  
111 7470.343750 0.72773900  
112 6804.421875 0.74979700  
113 6168.531250 0.77079800  
114 5564.382812 0.79071700  
115 4993.796875 0.80953600  
116 4457.375000 0.82725600  
117 3955.960938 0.84388100  
118 3489.234375 0.85943200  
119 3057.265625 0.87392900  
120 2659.140625 0.88740800  
121 2294.242188 0.89990000  
122 1961.500000 0.91144800  
123 1659.476562 0.92209600  
124 1387.546875 0.93188100  
125 1143.250000 0.94086000  
126 926.507812 0.94906400  
127 734.992188 0.95655000  
128 568.062500 0.96335200  
129 424.414062 0.96951300  
130 302.476562 0.97507800  
131 202.484375 0.98007200  
132 122.101562 0.98454200  
133 62.781250 0.98850000  
134 22.835938 0.99198400  
135 3.757813 0.99500300  
136 0.000000 0.99763000  
137 0.000000 1.00000000
  ```
  Then run `*/WPS/util/calc_ecmwf_p.exe`
  ```
     ./util/calc_ecmwf_p.exe
  ```
!!!TO DO!!!  
 add documentation for SST update 
 
NCEP SST was discontinued on Feb. 11, 2020. Here is a forum talking about replacements: https://github.com/wrf-model/WRF/issues/1159

A good replacement we found is NASA JPL SST (Sea Surface Temperature) dataset, whic is available from  June 1st, 2002 to the present. UC team already has a (kinda) [technical documentation](https://wiki.canterbury.ac.nz/display/UCHPC/Using+MUR+SST+data+to+nudge+WRF+simulations) for using NASA SST to run WRF. I will replicate the process and write something here.  



The following Drive API Credentials should be used when developing scripts to access or download files from the PO.DAAC Drive API.

The Drive API password is different than your Earthdata Login password.

Click the '?' for the FAQ to see examples of scripted API access, which include your Drive-specific login credentials.
Your PO.DAAC Drive API Credentials (WebDAV)

https://blog.sleeplessbeastie.eu/2017/09/04/how-to-mount-webdav-share/

```
Install required software

Install davfs2 package to mount WebDAV resource as regular file system.

$ sudo apt-get install davfs2

Mount WebDAV share using command-line

Create the mountpoint directory.

$ sudo mkdir /mnt/dav

```

4. **metgrid**  
4.1 run `metgrid.exe` with `Prefix='FILE', 'PRES'` in `namelist.wps`  
    ```
     ./metgrid/metgrid.exe
    ```
   To avoid possible errors and warnings, modify the interpolation methods in the metgrid table [`METGRID.TBL`](https://github.com/dongqi-DQ/WRF-Notes/blob/master/ERA5_initialisation/METGRID.TBL.ARW.ERA5)
   Outputs files: `met_em.d0*.yyyy-mm-dd_HH:MM:SS.nc`

## Step 3: Run WRF
1. link met_em files to `WRF/run` directory  
    ```
     ln -sf ../WPS/met_em.d0* .
    ```
2. run real.exe and then if no error occurred, run wrf.exe
