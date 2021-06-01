#!/bin/sh
NAMELIST_DIR="sst_files/ncep_daily_2017"

IDX=1


for filename in ${NAMELIST_DIR}/*; do
        [ -e "$filename" ] || continue
        echo $filename

	cdo -seltimestep,$IDX/$IDX rtgssthr.2017.grb $filename 
	 
	IDX=$((IDX+1))

        cdo showtimestamp $filename
              
done
