#!/bin/bash


# check if two arguments given
if [[ $# -ne 2 ]]
then 
	echo "Usage  <inputcsv> <outputdirectory>"
	exit 1
fi


input=$1
output=$2
# check if argument is valid
if [[ ! -f $input ]]
then
	# send error to standard error
	echo "Error! $input is not a valid input file name" 1>&2
	exit 1
fi

# create output directory only if it doesn't exist
mkdir -p $output

# write csv files for wells
awk -v out=$output '
        BEGIN {FS=OFS=","}
        {
                if (NR != 1 && (NF == 5 || NF ==  9) ) {  
                        well=substr($(NF-1),1,3);
			path=out"/"well".csv";
                        print $(NF-1), $(NF-2), $NF >> path;
                }
        }
' < $input


