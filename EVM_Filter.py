#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2017/8/22
"""

from lpp import * 
RAW = open(sys.argv[1], 'rU')
END = open(sys.argv[2], 'w')
if __name__ == '__main__':
	data = RAW.read()
	for e_b in data.split("\n\n"):
		if "GeneWise" in e_b or "assembler" in e_b:
			END.write(e_b + '\n\n')
		