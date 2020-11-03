# Using GNU to compile WRF and WPS

## Compile WRF - V4.2

<**Note**: there may be one library - netcdf fortran (lnetcdff) needs to be installed mannually>

(based on a [WRF V3.8 guide](https://www.enviroware.com/installing-and-running-wrf-3-8-on-linux-ubuntu-lts-16-04-with-intel-i7-8-core-cpu/))

1. Begining with WRF V4.0, WRF source code download is available [here](https://github.com/wrf-model/WRF/releases)   
2. Unzip the file `WRF-4.2.tar.gz` 
  ```
  tar xvzf WRF-4.2.tar.gz
  ```
3. Install required software as described in the [WRF V3.8 guide](https://www.enviroware.com/installing-and-running-wrf-3-8-on-linux-ubuntu-lts-16-04-with-intel-i7-8-core-cpu/)  
  ```
  sudo apt-get install csh gfortran m4 mpich libhdf5-mpich-dev libpng-dev libnetcdff-dev netcdf-bin ncl-ncarg
  ```
  install jasper:
  ```
  sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
  sudo apt update
  sudo apt install libjasper1 libjasper-dev
  ```
  
  
4. Set up environment
  - locate the netcdf library
    ```
    locate netcdf.inc
    ```
    which may return several locations, but only this one should be used (based on pervious successful configuration):  
    ```
    export NETCDF=/usr/local
    ```
  - locate the mpi lib  
    ```
    locate mpich/lib
    ```
    again, only this location is correct:  
    ```
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/mpich/lib
    ```
  - Set up WRF large file support 
    ```
    export WRFIO_NCD_LARGE_FILE_SUPPORT=1
    ```

5. Configure WRF
  - go to the directory where WRF source code is extracted
    ```
    cd WRF-V4.2
    ```
  - run the configure script
    ```
    ./configure
    ```
    there will be a list of options to choose:  
    ```
    Please select from among the following Linux x86_64 options:

    1. (serial)   2. (smpar)   3. (dmpar)   4. (dm+sm)   PGI (pgf90/gcc)
    5. (serial)   6. (smpar)   7. (dmpar)   8. (dm+sm)   PGI (pgf90/pgcc): SGI MPT
    9. (serial)  10. (smpar)  11. (dmpar)  12. (dm+sm)   PGI (pgf90/gcc): PGI accelerator
    13. (serial)  14. (smpar)  15. (dmpar)  16. (dm+sm)   INTEL (ifort/icc)
    17. (dm+sm)   INTEL (ifort/icc): Xeon Phi (MIC architecture)
    18. (serial)  19. (smpar)  20. (dmpar)  21. (dm+sm)   INTEL (ifort/icc): Xeon (SNB with AVX mods)
    22. (serial)  23. (smpar)  24. (dmpar)  25. (dm+sm)   INTEL (ifort/icc): SGI MPT
    26. (serial)  27. (smpar)  28. (dmpar)  29. (dm+sm)   INTEL (ifort/icc): IBM POE
    30. (serial)               31. (dmpar)                PATHSCALE (pathf90/pathcc)
    32. (serial)  33. (smpar)  34. (dmpar)  35. (dm+sm)   GNU (gfortran/gcc)
    36. (serial)  37. (smpar)  38. (dmpar)  39. (dm+sm)   IBM (xlf90_r/cc_r)
    40. (serial)  41. (smpar)  42. (dmpar)  43. (dm+sm)   PGI (ftn/gcc): Cray XC CLE
    44. (serial)  45. (smpar)  46. (dmpar)  47. (dm+sm)   CRAY CCE (ftn/cc): Cray XE and XC
    48. (serial)  49. (smpar)  50. (dmpar)  51. (dm+sm)   INTEL (ftn/icc): Cray XC
    52. (serial)  53. (smpar)  54. (dmpar)  55. (dm+sm)   PGI (pgf90/pgcc)
    56. (serial)  57. (smpar)  58. (dmpar)  59. (dm+sm)   PGI (pgf90/gcc): -f90=pgf90
    60. (serial)  61. (smpar)  62. (dmpar)  63. (dm+sm)   PGI (pgf90/pgcc): -f90=pgf90
    64. (serial)  65. (smpar)  66. (dmpar)  67. (dm+sm)   INTEL (ifort/icc): HSW/BDW
    68. (serial)  69. (smpar)  70. (dmpar)  71. (dm+sm)   INTEL (ifort/icc): KNL MIC
    ```
    Choose **34** for GNU compiler in the UC linux machine. Then choose compile for nesting (**option 1**)  
    ```Compile for nesting? (1=basic, 2=preset moves, 3=vortex following)```  
    You should see a message here indicating configuration is succesful, but if you see any NETCDF IO error, try this and re-configure:  
    ```export NETCDF_classic=1```  
    Successful configuration generates a configure file `configure.wrf`, where it is necessary to specify the information on the external libraries.  
    (A configuration file will be attached to check)  
    
6. Compile WRF
    ```
    ./compile em_real >& compile.log & 
    ```
   The ongoing compilation can be checked with:  
   ```
   tail -f compile.log 
   ```
   A successful compilation should give you a message in the end of `compile.log` like:  
   ```
   ==========================================================================
    build started:   xxxx
    build completed: xxxx
   --->                  Executables successfully built                  <---
 
    -rwxrwxr-x 1 rccuser rccuser 40225504 Jul 10 10:16 main/ndown.exe
    -rwxrwxr-x 1 rccuser rccuser 40110720 Jul 10 10:16 main/real.exe
    -rwxrwxr-x 1 rccuser rccuser 39619624 Jul 10 10:16 main/tc.exe
    -rwxrwxr-x 1 rccuser rccuser 44192256 Jul 10 10:15 main/wrf.exe

    ==========================================================================

   ```

Once the compilation completes, to check whether it was successful, you need to look for executables in the WRF/main directory:
```
    ls -ls main/*.exe
```
If you compiled a real case, you should see:
```
    wrf.exe (model executable)
    real.exe (real data initialization)
    ndown.exe (one-way nesting)
    tc.exe (for tc bogusing--serial only) 
```
If you compiled an idealized case, you should see:
```
    wrf.exe (model executable)
    ideal.exe (ideal case initialization) 
```
These executables are linked to 2 different directories:
```
    WRF/run
    WRF/test/em_real
```
You can choose to run WRF from either directory. 
 
## Compile WPS v4.2
  
WPS v4.2 is available to download [here](https://github.com/wrf-model/WPS/releases)  
<remove this later> Download geo-static files [here](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)

Decompress the file:
```
tar -ztfv WPSV4.2.TAR.gz
```

Go to `WPS-4.2`, edit the `config` file to make sure the WRF directory name is included:
```
154      standard_wrf_dirs="WRF WRF-4.0.3 WRF-4.0.2 WRF-4.0.1 WRF-4.0 WRFV3 WRF-4.2"
```
Note that `WRF-4.2` might not be in the list. 

Again, before configuration, set up environment:
  - netcdf library
    ```
    export NETCDF=/usr/local
    ```
  - mpi lib  
    ```
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/mpich/lib
    ```
  - WRF large file support 
    ```
    export WRFIO_NCD_LARGE_FILE_SUPPORT=1
    ```
  - Jasper for Grib2 I/O
    ```
    export JASPERLIB=/usr/lib/x86_64-linux-gnu
    export JASPERINC=/usr/include
    ```
Now start to configure WPS: `./configure` 

``` 
Will use NETCDF in dir: /usr/local
Found what looks like a valid WRF I/O library in ../WRF-4.2
Found Jasper environment variables for GRIB2 support...
  $JASPERLIB = /usr/lib/x86_64-linux-gnu
  $JASPERINC = /usr/include
------------------------------------------------------------------------
Please select from among the following supported platforms.

   1.  Linux x86_64, gfortran    (serial)
   2.  Linux x86_64, gfortran    (serial_NO_GRIB2)
   3.  Linux x86_64, gfortran    (dmpar)
   4.  Linux x86_64, gfortran    (dmpar_NO_GRIB2)
   5.  Linux x86_64, PGI compiler   (serial)
   6.  Linux x86_64, PGI compiler   (serial_NO_GRIB2)
   7.  Linux x86_64, PGI compiler   (dmpar)
   8.  Linux x86_64, PGI compiler   (dmpar_NO_GRIB2)
   9.  Linux x86_64, PGI compiler, SGI MPT   (serial)
  10.  Linux x86_64, PGI compiler, SGI MPT   (serial_NO_GRIB2)
  11.  Linux x86_64, PGI compiler, SGI MPT   (dmpar)
  12.  Linux x86_64, PGI compiler, SGI MPT   (dmpar_NO_GRIB2)
  13.  Linux x86_64, IA64 and Opteron    (serial)
  14.  Linux x86_64, IA64 and Opteron    (serial_NO_GRIB2)
  15.  Linux x86_64, IA64 and Opteron    (dmpar)
  16.  Linux x86_64, IA64 and Opteron    (dmpar_NO_GRIB2)
  17.  Linux x86_64, Intel compiler    (serial)
  18.  Linux x86_64, Intel compiler    (serial_NO_GRIB2)
  19.  Linux x86_64, Intel compiler    (dmpar)
  20.  Linux x86_64, Intel compiler    (dmpar_NO_GRIB2)
  21.  Linux x86_64, Intel compiler, SGI MPT    (serial)
  22.  Linux x86_64, Intel compiler, SGI MPT    (serial_NO_GRIB2)
  23.  Linux x86_64, Intel compiler, SGI MPT    (dmpar)
  24.  Linux x86_64, Intel compiler, SGI MPT    (dmpar_NO_GRIB2)
  25.  Linux x86_64, Intel compiler, IBM POE    (serial)
  26.  Linux x86_64, Intel compiler, IBM POE    (serial_NO_GRIB2)
  27.  Linux x86_64, Intel compiler, IBM POE    (dmpar)
  28.  Linux x86_64, Intel compiler, IBM POE    (dmpar_NO_GRIB2)
  29.  Linux x86_64 g95 compiler     (serial)
  30.  Linux x86_64 g95 compiler     (serial_NO_GRIB2)
  31.  Linux x86_64 g95 compiler     (dmpar)
  32.  Linux x86_64 g95 compiler     (dmpar_NO_GRIB2)
  33.  Cray XE/XC CLE/Linux x86_64, Cray compiler   (serial)
  34.  Cray XE/XC CLE/Linux x86_64, Cray compiler   (serial_NO_GRIB2)
  35.  Cray XE/XC CLE/Linux x86_64, Cray compiler   (dmpar)
  36.  Cray XE/XC CLE/Linux x86_64, Cray compiler   (dmpar_NO_GRIB2)
  37.  Cray XC CLE/Linux x86_64, Intel compiler   (serial)
  38.  Cray XC CLE/Linux x86_64, Intel compiler   (serial_NO_GRIB2)
  39.  Cray XC CLE/Linux x86_64, Intel compiler   (dmpar)
  40.  Cray XC CLE/Linux x86_64, Intel compiler   (dmpar_NO_GRIB2)

Enter selection [1-40] : 
```


We are using gfortran and serile compilation is sufficient, so we choose `1.  Linux x86_64, gfortran    (serial)` here. And if everything goes well, you will get: 
```
------------------------------------------------------------------------
Configuration successful. To build the WPS, type: compile
------------------------------------------------------------------------
```

Now check `configure.wps` file to make sure all the libraries are correct: 
```
WRF_LIB         =       -L$(WRF_DIR)/external/io_grib1 -lio_grib1 \
                        -L$(WRF_DIR)/external/io_grib_share -lio_grib_share \
                        -L$(WRF_DIR)/external/io_int -lwrfio_int \
                        -L$(WRF_DIR)/external/io_netcdf -lwrfio_nf \
                        -L$(NETCDF)/lib -lnetcdff -lnetcdf
```

Now WPS is ready to be compiled: 
```
./compile >& compile.log &
```

Use `tail` to check status:
```
tail -f compile.log
```

Once everything is done (successfully), you will see three executables in your WPS directory:
```
geogrid.exe -> geogrid/src/geogrid.exe
ungrib.exe -> ungrib/src/ungrib.exe
metgrid.exe -> metgrid/src/metgrid.exe 
```

If any of the exe files are missing, there must be something wrong during configuration or compilation process. NCAR provides a more detailed [tutorial](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php) which might give you some hints what went wrong.

Now we are ready to run WRF and WPS!








