#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/14
"""

import os,sys
from os.path import abspath

from lpp import *
from optparse import OptionParser
usage = '''usage: python2.7 %prog -i input_path -t [The type you want]'''
parser = OptionParser(usage =usage ) 
parser.add_option("-a", "--Anno", action="store", 
                  dest="Anno",
                  default = 'Anno', 
                  help="Annotation Table File")

parser.add_option("-p", "--PATH", action="store", 
                  dest="PATH", 
                  help="Input Path")
if __name__ == '__main__':
    (options, args) = parser.parse_args()
    ANNO = open(options.Anno,'rU')
    title_anno = ANNO.next().split("\t",1)[1]
    annotation_hash  = {}
    for line in ANNO:
        unigene,other = line.split("\t",1)
        annotation_hash[unigene] = other
        
        
    for e_path,paths,files in os.walk(options.PATH):
        for e_f in files:
            if e_f.endswith(".go"):
                
                condit_name = e_f.split(".")[0]
                out_path_name = e_path+'/'+condit_name+'/'
                if not os.path.exists(out_path_name):
                    os.makedirs(out_path_name)
                go_gene = Ddict()
                GO = open(e_path+'/'+e_f,'rU')
                for line in GO:
                    line_l = line.strip().split("\t")
                    go_gene[line_l[-1]][line_l[0]] = ""
                    
                END = open(out_path_name+'/'+condit_name+".EnrichGO_Annotation.xls",'w')
                END.write("GOID\tDescription\tUnigene\t"+title_anno)
                SIG = open(  e_path+'/'+condit_name+ "_go_enrich.tsv",'rU'  )

                for line in SIG:
                    line_l = line.split("\t")
                    go_id,go_name = line_l[0],line_l[-2]
                    for each_gene in go_gene[go_id]:
                        out_cache = [ go_id,go_name,each_gene,annotation_hash[each_gene]  ]
                        END.write('\t'.join(  out_cache  )  )
                        
                        
                        
                        
                        
                        
