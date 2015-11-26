#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/26
"""
from lpp import *
from multiprocessing import Pool
cpu = 12
pool = Pool(cpu)
RAW = open(sys.argv[1],'rU')
title = RAW.next()
input_hash = {}
for i in xrange(0,cpu):
    out_path = os.path.abspath(  "./%s_out/"%(i)  )+'/'
    if not os.path.exists(  out_path):
        os.makedirs( out_path )
        input_hash[i] = open(out_path+"cache.tsv",'w')
        input_hash[i].write( title  )
        
j=0
for line in RAW:
    j+=1
    num = j%cpu
    input_hash[num].write(line)
    
def run(  num ):
    os.system( "cd %s && KAKS.py -i %s -o out/"%(  "./%s_out/"%(num    ),input_hash[num].name   )  )
map(run,xrange(0,cpu))

output_path = os.path.abspath( sys.argv[2] )
if  not os.path.exists(output_path):
    os.makedirs(output_path)
END= open(output_path+'/KAKS_Result.tsv','w')

END.write(open( out_path+'out/KAKS_Result.tsv','rU').next() )

for i in xrange(0,cpu):
    RAW = open( out_path+'out/KAKS_Result.tsv','rU'  )
    RAW.next()
    END.write(RAW.read())
        
    