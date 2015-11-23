#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/11/21
"""

from lpp import *
RAW = open(sys.argv[1],'rU')
END = open(sys.argv[1]+'1','w')
END.write(RAW.next())
DATA = block_reading(RAW, "\n\n")
print(DATA.next())
