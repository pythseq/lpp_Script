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
#from Dependcy import *

db_number = sys.argv[1]
r = redis.Redis(host='localhost',port=6379,db=int(db_number))
r.flushall()
DATA = open(sys.argv[2],'w')
FASTA = fasta_check(open(sys.argv[3],'rU'))
data_hash = Ddict()


for t,s in FASTA:

    t = t[1:].strip()
    name = t.split()[0]

    data_hash[name]["Name"]=name
    data_hash[name]["Sequence"]=re.sub("\s+","",s)
    data_hash[name]["Length"]=str(len(re.sub("\s+","",s)))

DATA.write(Redis_trans(data_hash))



