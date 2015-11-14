#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys
from os.path import abspath
sys.path.append( os.path.split(abspath(__file__))[0]+'/../Lib/' )
from lpp import *
from Dependcy import *
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-d", "--Database", action="store",
                  dest="DB_FILE",

                  help="Database File")


parser.add_option("-p", "--Path", action="store",
                  dest="Path",

                  help="Diff Path")
if __name__ == '__main__':
    (options, args) = parser.parse_args()
    data_hash = Ddict()
    DB_FILE = open( os.path.abspath(options.DB_FILE),'a')
    for a,b,c in os.walk(options.Path):
        for e_f in c:
            if e_f.endswith(".end") and "_up" not in e_f and "_down" not in e_f:
                condition_name = "Compare "+e_f.split(".")[0].replace("__"," vs ")
                RAW = open(a+'/'+e_f,'rU')
                RAW.next()
                for line in RAW:
                    line_l = line.strip().split("\t")
                    name = line_l[0]
                    out_cache = []
                    log2foldchange = "log2Foldchange:"+line_l[-4]
                    out_cache.append(log2foldchange)
                    
                    pval = "pval:"+line_l[-3]
                    qval = "fdr:"+line_l[-2]
                    out_cache.append(pval)
                    out_cache.append(qval)
                    data_hash[name][condition_name]= ' | '.join( out_cache )
                    data_hash["title"][condition_name]=""
                    new_conname = condition_name+"_"+line_l[-1]
                    data_hash["title"][new_conname]=""
                    data_hash[name][new_conname]= ' | '.join( out_cache )
                    
                    
                    
    #for data in data_hash[name]:
        #data_hash["title"][data] = ""    
    DB_FILE.write(Redis_trans(data_hash))


