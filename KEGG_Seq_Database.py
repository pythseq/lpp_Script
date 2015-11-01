#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
from optparse import OptionParser
from lpp import *
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--SEQ", action="store",
                  dest="SEQ",

                  help="KEGG Protein seq Database")
if __name__ == '__main__':
    (options, args) = parser.parse_args()
    data_hash_all = Ddict()
    (options, args) = parser.parse_args()
    KEGG = fasta_check(open(options.SEQ,'rU'))
    for t,s in KEGG:
        name,anno  = t.strip().split(None,1)
        data_hash_all[name]["Annotation"] = anno
        length = len(re.sub("\s+","",s))
        data_hash_all[name]["Length"] = str(length)
    END = open("cache.redis",'w')
    END.write(Redis_trans(data_hash_all))
    
