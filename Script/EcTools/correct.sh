#!/bin/bash -x

#Make sure all of the Nucmer tools are in your path

set -e 

source ~/.bashrc

##SET THE FOLLOWING PARAMETERS

#path to correct script in pbtools repo
CORRECT_SCRIPT=$ECTOOLS_HOME/pb_correct.py
TMPDIR="./tmp"
#pre filter delta file
PRE_DELTA_FILTER_SCRIPT=$ECTOOLS_HOME/pre_delta_filter.py

#smallest alignment allowed, filter out alignments smaller than this
#set this a few bp short of the short-read length
MIN_ALIGNMENT_LEN=200

#Allow % from the ends of the fragments to be wiggle room 
#(for determining proper overlaps)
WIGGLE_PCT=0.05

#pct of read length for alignment to be considered contained
CONTAINED_PCT_ID=0.80

#path to high identity unitigs
UNITIG_FILE=$UNITIG

#Trim out regions with lower identity than
CLR_PCT_ID=0.96

#Minimum read length to output after splitting/trimming
MIN_READ_LEN=3000

#Number of bases without a match after which nucmer breaks the alignment.
#Increase for better alignments but at the cost of dramatically
#increased runtime 
#Small genomes (10's of MB) can up this to 10000
NUCMER_BREAK_LEN=2000

##Filter the delta file for proper overlaps before doing LIS in delta-filter
#
#Depending on the quality of the data, you may want to ensure
#that only proper overlapping alignments are used for correction.
#If the initial short read assembly is very good (ex. 100kb contig N50)
#you probably want to ensure proper overlaps.
#If the initial assembly is not very contiguous, requiring
#proper overlaps may hinder correction.
#'true' setting is most useful for short genomes with high coverage.
PRE_DELTA_FILTER=true

###Done parameters

FILE=$INPUT

ORIGINAL_DIR=`pwd`


nucmer --maxmatch -l 11 -b ${NUCMER_BREAK_LEN} -g 1000 -p ${FILE} ${FILE} ${UNITIG_FILE}



FILTERED_DELTA=${FILE}.delta
if [[ "$PRE_DELTA_FILTER" == true ]]
then
    FILTERED_DELTA=${FILE}.delta.pre
    python ${PRE_DELTA_FILTER_SCRIPT} ${FILE}.delta ${WIGGLE_PCT} ${CONTAINED_PCT_ID} ${MIN_ALIGNMENT_LEN} ${FILTERED_DELTA}

fi

delta-filter -l $MIN_ALIGNMENT_LEN -i 70.0 -r ${FILTERED_DELTA} > ${FILTERED_DELTA}.r



show-coords -l -H -r ${FILTERED_DELTA}.r > ${FILTERED_DELTA}.r.sc



show-snps -H -l -r ${FILTERED_DELTA}.r > ${FILTERED_DELTA}.snps



python ${CORRECT_SCRIPT} ${FILE} ${FILTERED_DELTA}.snps ${FILTERED_DELTA}.r.sc ${CLR_PCT_ID} ${MIN_READ_LEN} ${FILE}

cp ${FILE}.cor.fa $OUTPUT.cor.fa
cp ${FILE}.cor.pileup $OUTPUT.cor.pileup

