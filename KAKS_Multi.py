#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/26
"""
from lpp import *
from multiprocessing import Pool
pool = Pool(64)
RAW = open(sys.argv[1],'rU')
title = RAW.next()
input_hash = {}
for i in xrange(0,64):
    out_path = os.path.abspath(  "./%s_out/"%(i)  )
    if not os.path.exists(  out_path):
        os.makedirs( out_path )
        input_hash[i] = open(out_path+"cache.tsv",'w')
        input_hash[i].write( title  )
        
j=0
for line in RAW:
    j+=1
    num = j%64
    input_hash[num].write(line)
    
def run(  num ):
    os.system( "cd %s && KAKS.py -i %s -o out/"%(  "./%s_out/"%(num    ),input_hash[num].name   )  )
    
pool.map(run,xrange(0,64))
        
    