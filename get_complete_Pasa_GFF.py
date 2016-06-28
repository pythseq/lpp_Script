#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2016/6/28
"""

from lpp import *
RAW = open(sys.argv[1])
all_complete = File_dict(open(sys.argv[2],'rU'))
END = open(sys.argv[3],'w')
for line in RAW:
    asid = re.findall( "Target\=(\s+)",line)
    if asid:
        asid = asid[0]
        if asid in all_complete:
            END.write(line)