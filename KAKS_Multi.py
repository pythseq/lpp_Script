#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/26
"""
from lpp import *
from multiprocessing import Pool
cpu = 16

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
    
    num = j%cpu
    input_hash[num].write(line)
    j+=1
def run( ( num ,name) ):
    name = name.name
    path = os.path.split(os.path.abspath(name))[0]
    os.system( "KAKS.py -i %s -o %s/out/"%(  name,path   )  )
pool = Pool(cpu)

data_list = []
for i in xrange(0,cpu):
    data_list.append( [ i,  input_hash[i] ]   )
#map(  run,data_list  )
pool.map( run,data_list )
output_path = os.path.abspath( sys.argv[2] )
if  not os.path.exists(output_path):
    os.makedirs(output_path)
END= open(output_path+'/KAKS_Result.tsv','w')

END.write(open( out_path+'out/KAKS_Result.tsv','rU').next() )

for i in xrange(0,cpu):
    RAW = open( out_path+'out/KAKS_Result.tsv','rU'  )
    RAW.next()
    for line in RAW:
        END.write(line)
        
    