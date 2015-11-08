#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys,redis
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import *


DATA = open(sys.argv[1],'a')
FASTA = fasta_check(open(sys.argv[2],'rU'))
data_hash = Ddict()
data_hash["title"]["Name"]=""
data_hash["title"]["Sequence"]=""
data_hash["title"]["Length"] = ""
for t,s in FASTA:

    t = t[1:].strip()
    name = t.split()[0]

    data_hash[name]["Name"]=name
    data_hash[name]["Sequence"]=re.sub("\s+","",s)
    data_hash[name]["Length"]=str(len(re.sub("\s+","",s)))

DATA.write(Redis_trans(data_hash))



