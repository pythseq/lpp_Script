#!/usr/bin/env python
#coding:utf-8
"""
  Author:   -->
  Purpose: 
  Created: 2015/10/24
"""
from lpp import *
RAW = open(sys.argv[1],'rU')
END = open(sys.argv[2],'w')
data_hash = {}
for line in RAW:
    if "\ttranscript\t" in line:
        continue
    line_l = line.split("\t")
    line_l[2] = "EST_match"
    name =re.search("Parent\=(\S+)",line_l[-1]).group(1)
    loc = int(line_l[4]) - int(line_l[3])
    append = loc - loc%3-1
    if name not in data_hash:
        data_hash[name] =""
        start = 1
        end = start+append
    else:
        start = end+1
        end = start +append
        
    END.write("\t".join(line_l[:-1]))
    END.write( "\tID=%s;Target=%s %s %s\n"%(name,name+"_est",start,end)    )
    