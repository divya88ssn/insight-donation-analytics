#!/bin/bash

#pass input and output file location to the source code
#python ./master_scheduler.py $1 $2 $3
python src/master_scheduler.py "../input/itcont.txt" "../input/percentile.txt" "../output/repeat_donors.txt"
