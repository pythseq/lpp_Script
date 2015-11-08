#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys

sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import *
DB_FILE = open(os.path.abspath(sys.argv[1]),'a')
NR_ANNO_DETAIL = open(sys.argv[2],'rU')
data_hash = Ddict()
#NR_ANNO_DETAIL.next()
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

