#!/bin/bash

XYZ_DIR=/home/pi/nano/3w_files
CMP_DIR=/home/pi/nano/3w_analysis/regression_test
TO_GCODE_EXE=/home/pi/nano/3w_analysis/c/build/to_gcode.out


cd $XYZ_DIR
for i in *.3w; do
	EXPECTED_FILE=$CMP_DIR/`echo $i | sed -e s/3w/gcode/`
	$TO_GCODE_EXE $i | diff $EXPECTED_FILE -;
done
