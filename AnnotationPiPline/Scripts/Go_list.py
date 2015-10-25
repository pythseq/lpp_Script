#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/23
"""
import sys
RAW = open(sys.argv[1],'rU')
END = open(sys.argv[2],'w')
RAW.next()
END.write("Gene\tFunction\n")
has = {}
for line in RAW:
	line_l = line.split("\t")
	if line.startswith("GO:"):
		function =line_l[1]
	else:
		gene = line_l[3]
		output = gene+"\t"+function+'\n'
		if output in has:
			continue
		END.write(gene+"\t"+function+'\n')
		has[output] = ""
		
