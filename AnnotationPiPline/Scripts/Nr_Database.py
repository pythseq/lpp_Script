#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys
from os.path import abspath
sys.path.append( os.path.split(abspath(__file__))[0]+'/../Lib/' )
from lpp import *
from Dependcy import *
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-d", "--Database", action="store",
                  dest="DB_FILE",

                  help="Database File")


parser.add_option("-n", "--Nr", action="store",
                  dest="NR",

                  help="Nr Ghostz Aligment Result")
if __name__ == '__main__':
	(options, args) = parser.parse_args()

	DB_FILE = open( os.path.abspath(options.DB_FILE),'a')
	
	NR_ANNO_DETAIL = open(   os.path.abspath(  options.NR ),'rU'   ) 
	
	data_hash = Ddict()
	for line in NR_ANNO_DETAIL:
		line_l = line[:-1].split("\t")
		name = line_l[0].split()[0]
		6[name]["Nr_Hit"] = line_l[1]+" "+line_l[2]
		data_hash[name]["Nr_Eval"] = line_l[-2]
		data_hash[name]["Nr_Bit_Score"] = line_l[-1]
		data_hash[name]["Nr_Identity"] = line_l[2]
		data_hash[name]["Nr_StartQuery"] = line_l[6]
		data_hash[name]["Nr_EndQuery"] = line_l[7]
		data_hash[name]["Nr_Mismatch"] = line_l[5]
		data_hash[name]["Nr_EndSubj"] = line_l[9]
		data_hash[name]["Nr_StartSubj"] = line_l[8]
	for data in data_hash[name]:
		data_hash["title"][data] = ""	
	DB_FILE.write(Redis_trans(data_hash))


