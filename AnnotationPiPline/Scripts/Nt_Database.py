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


parser.add_option("-n", "--Nt", action="store",
                  dest="NT",

                  help="Nt Ghostz Aligment Result")
#NR_ANNO_DETAIL.next()
if __name__ == '__main__':
	(options, args) = parser.parse_args()
	DB_FILE = open( os.path.abspath(options.DB_FILE),'a')
	
	NR_ANNO_DETAIL = open(   os.path.abspath(  options.NT ),'rU'   ) 	
	for line in NR_ANNO_DETAIL:
		line_l = line[:-1].split("\t")
		name = line_l[2].split()[0]
		data_hash[name]["Nt_Hit"] = line_l[5]+" "+line_l[6]
	
		data_hash[name]["Nt_Eval"] = line_l[12]
		data_hash[name]["Nt_Query_From"] = line_l[13]
		data_hash[name]["Nt_Query_To"] = line_l[14]
		data_hash[name]["Nt_Hit_From"] = line_l[15]
		data_hash[name]["Nt_Hit_To"] = line_l[16]
		data_hash[name]["Nt_BitScore"] = line_l[10]
		data_hash[name]["Nt_Identity"] = str(int(line_l[-6])*100.0/int(line_l[3]))
		
		
		
	for data in data_hash[name]:
		data_hash["title"][data] = ""
		
	DB_FILE.write(Redis_trans(data_hash))

