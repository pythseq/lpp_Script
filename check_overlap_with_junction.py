#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2016/6/24
"""

from  lpp import *
import os
#data = sys.stdin
data = os.popen("show-coords  -oqTH  %s "%(os.sys.argv[1]))
all_need = {}
for line in data:
    line_l = line[:-1].split("\t")
    q_name = line_l[-2]
    q_start,q_end = sorted( [ int(line_l[2]), int(line_l[3])  ] )

    data_set = set( xrange(q_start,q_end+1   ) )
    if  q_name not in all_need:
        all_need[ q_name] = [data_set]
    else:
        removed= []
        
        for each_set  in all_need[q_name]:
            if each_set & data_set == each_set and each_set!=data_set:
                removed.append(each_set)
        for i in removed:
            all_need[q_name].remove(i)
        append_tag = 0
        for each_set  in all_need[q_name]:
            
            if each_set & data_set == data_set and each_set!=data_set:
                append_tag=1
                
                
        if append_tag==0:
            
            all_need[q_name].append( data_set )

align = sys.stdin
for  line in align:
    line_l = re.split("\s+\|*\s*",line[:-1])
    q_name = line_l[-2]
    
    q_start,q_end = sorted( [ int(line_l[2]), int(line_l[3])  ] )   
    if q_name not in all_need:
        #print(line),
        pass
    else:
        print("q_name is "+q_name)
        
        data_set = set( xrange(q_start,q_end+1   ) )
        tag=0
        for each_set in all_need[ q_name ]:
            
            if data_set in each_set and  data_set!=each_set:
                new_data = sorted(list(data_set))
                
                #print( q_start,q_end  )
                #print( "nucmer is %s %s"%(data_set[0],data_set[-1]))
                tag =1
        if tag==1:
            print(line),
                