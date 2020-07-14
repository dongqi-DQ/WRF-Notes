# Compile WRF - V4.2  
## Using GNU  

(based on a [WRF V3.8 guide](https://www.enviroware.com/installing-and-running-wrf-3-8-on-linux-ubuntu-lts-16-04-with-intel-i7-8-core-cpu/))

1. Begining with WRF V4.0, WRF source code download is available [here](https://github.com/wrf-model/WRF/releases)   
2. Unzip the file `WRF-4.2.tar.gz` 
  ```
  tar xvzf WRF-4.2.tar.gz
  ```
3. Install required software as described in the [WRF V3.8 guide](https://www.enviroware.com/installing-and-running-wrf-3-8-on-linux-ubuntu-lts-16-04-with-intel-i7-8-core-cpu/)  
  ```
  sudo apt-get install csh gfortran m4 mpich libhdf5-mpich-dev libpng-dev libjasper-dev libnetcdff-dev netcdf-bin ncl-ncarg
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
 
# Compile WPS v4.2
  
WPS v4.2 is available to download [here](https://github.com/wrf-model/WPS/releases)
Download geo-static files [here](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)
