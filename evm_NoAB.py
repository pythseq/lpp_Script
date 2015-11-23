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

DATA = RAW.read().split("\n\n")
print(DATA[0])
