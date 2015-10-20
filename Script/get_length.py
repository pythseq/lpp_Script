#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/20
"""
from lpp import *
RAW = fasta_check(open(sys.argv[1],'rU'))
END = open(sys.argv[2],'w')
for t,s in RAW:
	END.write(t[1:-1].split()[0]+'\t%s\n'%(len(re.sub("\s+",'',s))) )


