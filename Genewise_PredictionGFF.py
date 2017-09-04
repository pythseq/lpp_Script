#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/10/20
"""

from lpp import *
from optparse import OptionParser



if __name__ == '__main__':
    usage = '''usage: python2.7 %prog [options] '''
    parser = OptionParser(usage =usage )    
  
    parser.add_option("-i", "--genewise", action="store",
                      dest="genewise",
                      help="Genese Result!!")
    parser.add_option("-o", "--output", action="store",
                      dest="output",
                      help="GFF Parse output!!")    
    
    (options, args) = parser.parse_args()

    genewise = options.genewise
    output = options.output  
    END = open(output,'w')
    CACHE = open( "Cache.gff", 'w')
    RAW = re.split("//\nBits",open(genewise,'rU').read())
    j=0
    for e_b in RAW:
        if "STRG" not in e_b:
            
            continue
        mrna_name = re.search("(STRG\S+)", e_b).group(1)
        gene_name =  mrna_name.rsplit(".", 1)[0]
        data_b = e_b.split("\n//\n")
        gff_b = data_b[-1]
        cds_data = []
        exon_data = []
        
      
        for line in gff_b.split("\n"):
            if not line:
                continue
        
            gff_list = line.split("\t")
            if gff_list[2] == "intron":
                continue
            
            
            seq_name = gff_list[0]
        
            subjname,loc_append = seq_name.rsplit("__",1)
            loc_append  = int(loc_append)
            gff_list[0] = subjname
            gff_list[3] = int(gff_list[3]) + loc_append
            gff_list[4] = int(gff_list[4]) + loc_append
            gff_list[3],gff_list[4] = sorted([ gff_list[3],gff_list[4] ])
            gff_list[3] = str(gff_list[3])
	    gff_list[4] =  str(gff_list[4])
            
            
            if gff_list[2] == "match":
                gff_list[2] = "mRNA"
                gff_list[-1] = "ID=%s;Parent=%s" % (mrna_name,gene_name)
                END.write("\t".join(gff_list)+'\n')
            if gff_list[2] == "cds":
                gff_list[2] = "exon"
                exon_data.append("\t".join(gff_list[:-1]))
                gff_list[2] = "CDS"
                cds_data.append( "\t".join(gff_list[:-1]))
        
                
        
        cds_data = iter(sorted( cds_data, key = lambda x: int( x.split("\t")[3] ) ) )
        exon_data = iter(sorted( exon_data, key = lambda x: int( x.split("\t")[3] ) ) )
        i = 1
        for key in exon_data:
            END.write(key + '\t' + "ID=%s.Exon%s;Parent=%s\n" % (mrna_name, i, mrna_name))
            
            END.write(cds_data.next() + '\t' + "ID=%s.Exon%s;Parent=%s\n" % (mrna_name, i, mrna_name))
        END.write("\n")
