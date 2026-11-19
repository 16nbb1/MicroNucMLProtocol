#!/bin/bash

#source $HOME/env/bin/activate

# Declare variables. At minimum, users need to pass the input directory and the desired output location for the json
src=$1_Processed
dst=$2
mode=”ALL”
conf=0.7
parent=“edge”
apop=True
apop_cnt=5 

outpath=$(dirname "$2")
mkdir $outpath

# Running the tool itself --> *** WILL NEED TO POINT THIS TO A DIFF LOCATION!!!** LIKELY $HOME/ETC..
#python $HOME/MicroNuclei_Detection/src/compute_scripts/image_process.py \
#--src src –dst dst \
#–mode mode --conf conf --parent parent --apop apop --apop_cnt apop_cnt 
