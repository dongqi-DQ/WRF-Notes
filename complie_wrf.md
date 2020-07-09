# Compile WRF - V4.2  
## Using GNU  

(based on a [WRF V3.8 guide](https://www.enviroware.com/installing-and-running-wrf-3-8-on-linux-ubuntu-lts-16-04-with-intel-i7-8-core-cpu/))

1. Download WRF source code [here](https://github.com/wrf-model/WRF/releases)   
2. Unzip the file ```WRF-4.2.tar.gz``` 
  ```
  
  ```
3. Install required software as described in the [WRF V3.8 guide](https://www.enviroware.com/installing-and-running-wrf-3-8-on-linux-ubuntu-lts-16-04-with-intel-i7-8-core-cpu/)  
4. Set up environment:  
  ```
  export NETCDF=/usr
  export WRFIO_NCD_LARGE_FILE_SUPPORT=1
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/mpich/lib
  ```

5. 

If have netcdf issue, try this  
```export NETCDF_classic=1```
