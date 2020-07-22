echo 'write "[centre]_[dataDate]_[dataType]_[levelType]_[step].grib[edition]";' > split.rule

for f in *sfc.grib
do
	echo "processing $f"
	grib_filter split.rule $f
done

for f in *ml.grib
do
	echo "processing $f"
	grib_set -s deletePV=1,edition=1 $f ${f}1
	grib_filter split.rule ${f}1
	rm ${f}1
done
