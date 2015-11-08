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
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


DB_FILE = open(os.path.abspath(sys.argv[1]),'a')

NR_ANNO_DETAIL = open(sys.argv[2],'rU')

data_hash = Ddict()
for line in NR_ANNO_DETAIL:
	line_l = line[:-1].split("\t")
	name = line_l[0]
	data_hash[name]["Nr_Hit"] = line_l[1]+" "+line_l[2]
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


