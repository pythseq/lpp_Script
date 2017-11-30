#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/11/4
"""
import os
from lpp import *


def Pathway_Enrichment():


    enrich_result = []
    p_value_list = []
    R_DATA = open("/tmp/%s.dat" % (os.getpid()), 'w')
    R_DATA.write("Pathway\tAllDif\tAllGene\tAll_In\tDiff_In\n")    
    for each_pathway in all_pathway:
        if not len( diff_gene_pathway[ each_pathway  ] ):
            continue
       
        if each_pathway in diff_gene_pathway:        
            
            R_DATA.write( "%s\t%s\t%s\t%s\t%s\n" % (each_pathway,len( all_diff_geneinpathway) , len( all_geneinpathway ),len( all_pathway[ each_pathway  ]  ) ,  len( diff_gene_pathway[ each_pathway  ] )) )
    R_DATA.close()
    RSCRIPT = open("/tmp/Phyer.%s.R" % (os.getpid()), 'w')

    RSCRIPT.write( """library(qvalue)         
Data<-read.delim( "%s", header=TRUE, stringsAsFactors=TRUE ) 
Data$pval<- 1- phyper(Data$Diff-1, Data$AllDif, Data$AllGene-Data$Diff_In, Data$All_In)"""% (
                                           R_DATA.name,
                                           
                                       ) + """

Data$padj<- p.adjust(Data$pval, method="BH")
Data$qvalue<- qvalue(Data$pval,lambda=0)$qvalues
Data = Data[ Data$padj<0.05,  ]
write.table(Data,row.names=F,file='%s',quote=FALSE,sep='\t')

        """% ( options.output) )
    RSCRIPT.close()
    os.system( "Rscript %s" % (RSCRIPT.name))


    return RSCRIPT.name
if __name__ == "__main__":
    usage = '''usage: python2.7 %prog [options]
			        '''
    parser = OptionParser(usage =usage )  
    parser.add_option("-t", "--Table", action="store",
                      dest="Table",
                      help="KEGG Annotation TSV")		
    parser.add_option("-i", "--Input", action="store",
                      dest="Input",
                      help="Database Name")
    parser.add_option("-o", "--OUTPUT", action="store",
                      dest="output",
                      help="output File Name")  
    parser.add_option("-a", "--Anno", action="store",
                      dest="Annotation",
                      help="Annotation Result")  	
    (options, args) = parser.parse_args()

    
    all_pathway = Ddict()
    diff_gene_pathway = Ddict()
    RAW = open(options.Input, 'rU')
    i = 0
    line_l = RAW.next().strip().split("\t")
    for key in line_l:
        i += 1
        if key.lower() == "id":
            break
    all_diff_gene = File_dict(open(options.Input,'rU')).read(i, i)
    all_diff_geneinpathway = {}
    all_geneinpathway = {}
    check_path( os.path.dirname( options.output) )
    all_annotation  = {}
    ANNO = open( options.Annotation,'w' )
    ANNO.write("Unigene\tEnrichedPathwayID\tEnrichedPathwayName\t"+"\t".join( RAW.next().split("\t")[1:]) )
    RAW = open( options.Table,'rU' )
    for line in RAW:
        line_l = line[:-1].split("\t")
        if not line_l[-2]:
            continue
        pathway_list  = line_l[-2].split("||")
        if line_l[0] in all_diff_gene:
            all_annotation[line_l[0]] = "\t".join(  line_l[1:]  )

            for each_pathway in pathway_list:
    
                diff_gene_pathway[ each_pathway][ line_l[0] ] = ""
                all_diff_geneinpathway[ line_l[0] ] = ""
        all_geneinpathway[ line_l[0] ] = ""
            
        for each_pathway in pathway_list:    
            all_pathway[ each_pathway ][ line_l[0] ] = ""

    all_enrich = Pathway_Enrichment()
    #for pathway in all_enrich:
        #for geneId in all_enrich[ pathway ]:
            #ANNO.write(  geneId+'\t'+pathway+'\t'+all_annotation[geneId] +'\n' )
