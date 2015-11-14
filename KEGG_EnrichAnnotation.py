#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/14
"""

import os,sys
from os.path import abspath
from optparse import OptionParser
from lpp import *

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
            if e_f.endswith(".m4"):
                condit_name = e_f.split(".")[0]
                all_need_gene ={}
                for line in open(   e_path+'/'+e_f ,'rU'):
                    gene = line.split()[0]
                    
                    all_need_gene[gene] = ""
                PATHWAY = open( e_path+"/"+condit_name+"_Pathway.tsv")
                pathway_gene = Ddict()
                for line in PATHWAY:
                    line_l = line.split("\t")
                    if line_l[0] in all_need_gene:
                        pathway_gene[line_l[1]][line_l[0]] = ""
                SIG = open(e_path+'/'+condit_name+".PathwaySig.sigend",'rU')
                SIG.next()
                END = open(e_path+'/'+condit_name+".Pathway_EnrichAnnotation.xls",'w')
                END.write("\tPathwayID\tPathwayName\tUnigene"+title_anno)
                print(pathway_gene)
                for line in SIG:
                    
                    line_l = line.split("\t")
                    pathway_id,pathway_name = line_l[:2]
                    for each_gene in pathway_gene[pathway_id]:
                        out_cache = [ pathway_id,pathway_name,each_gene,annotation_hash[each_gene]  ]
                        END.write('\t'.join(  out_cache  )  )
                        
                        
                        
                        
                        
                        
