#!/usr/bin/python
#coding:utf-8
# Author:  LPP --<lpp1985@hotmail.com>
# Purpose: 
# Created: 2011/4/28
from lpp import *
RAW = open( sys.argv[1] )
END = open(sys.argv[1]+'.top1','w')

		
already = Ddict()
for line in RAW:
	line_l = line.split('\t')

	already[line_l[2]][line_l[6]] = line
for key in already:
	key2 = sorted(already[key])[-1]
	END.write(already[key][key2])
