#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/11/21
"""
import sys,shlex,os,subprocess
from ConfigParser import ConfigParser
import redis
import tempfile
from  termcolor import colored
from lpp import *
from optparse import OptionParser
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--Input", action="store",
                  dest="Input",

                  help="Input Fasta Sequence")
parser.add_option("-o", "--Output", action="store",
                  dest="output",

                  help="Output File")

parser.add_option("-d", "--Database", action="store",
                  dest="Database",

                  help="Database Location")
parser.add_option("-e", "--Evalue", action="store",
                  dest="Evalue",

                  help="Evalue !")
parser.add_option("-n", "--DBName", action="store",
                  dest="dbname",

                  help="DB Name")
parser.add_option("-t", "--Type", action="store",
                  dest="type",

                  help="AlignType, blastx or blastp ,default is blastp",
                  default ="blastp"
                  )

if __name__=="__main__":
    (options, args) = parser.parse_args()
    Input = options.Input
    OUTPUT = options.output
    Database = options.Database
    Path = os.path.split(OUTPUT)[0]
    Type = options.type
    if Type not in ["blastx","blastp"]:
        print(colored(  "Type is error! must be blastx or blastp!!!","red"))
        sys.exit()
    if not Path:
        Path="./"
    if not os.path.exists(Path):
        os.makedirs(Path)
    Path = Path+'/'
    E_value = options.Evalue
    query_length = {}
    RAW = fasta_check(open(Input,'rU'))
    for t,s in RAW:
        name = t.split()[0][1:]
        length = str(len(re.sub("\s+", "", s)))
        query_length[name]=length
    temp_name = str(os.getpid())
    tmp_file_name = Path+temp_name
    commandline = """     diamond %s -q %s -d %s  -e %s  --max-target-seqs 1  -p 64 -a %s"""%( 
        Type,
        Input,

        Database,
        E_value,
        OUTPUT 
    )
    os.system(commandline)

