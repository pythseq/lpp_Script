#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2016/7/21
"""
from lpp import *
RAW = open(sys.argv[1],'rU')
END = open(sys.argv[2],'w')
all_has = {}
OLD_ID = ""
i=0
cache = []
for line in RAW:
    
    ID = re.search("ID=([^\;]+)",line).group(1)
    
    line_l = line.strip().split("\t")
    end = line_l[4]
    
    if not OLD_ID:
        OLD_ID= ID 
        start = line_l[3]
        i+=1
    attribute = "ID=exons.gene%s;Parent=Protein%s\n"%(i,i)
    line_l[2]="exon"
    
    cache.append(   '\t'.join(line_l[-1])+'\t'+attribute  )
    attribute = "ID=cds.gene%s;Parent=Protein%s\n"%(i,i)
    line_l[2]="cds"   
    cache.append(   '\t'.join(line_l[-1])+'\t'+attribute  )
    
    old_data = line_l
    print(ID ,OLD_ID )
    
    if ID != OLD_ID and OLD_ID!='':
        OLD_ID=ID
        
        line_l =old_data
        line_l[3]=start
        line_l[4] = end

        line_l[2] = "gene"
        END.write("\t".join(line_l))
        attribute = "ID=gene%s;Name=gene%s\n"%(i,i)
        END.write('\t'+attribute+'\n')
        line_l[2] = "mRNA"
        attribute = "ID=Protein%s;Parent=gene%s\n"%(i,i)
        END.write("\t".join(line_l)+'\t'+attribute+'\n')
        i+=1
        END.write(  "".join(cache) )
        start = line_l[3]
        
        
        
        
        cache = []
        