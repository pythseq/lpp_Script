#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/11/4
"""
import os
from lpp import *
def enrichand_pvalue( CACHE,diff_gene, total_anno_gene,output ):
    output = os.path.abspath(output)
    name = CACHE.name
    SCRIPT = open("/tmp/hyper%s.R"%(  os.getpid() ),'w')
    SCRIPT.write("library(qvalue) \n")
    SCRIPT.write("""countsTable <- read.delim(  "%s", header=TRUE, stringsAsFactors=TRUE )\n"""%(name) )
    SCRIPT.write(
        """ countsTable$pvalue =  1- phyper(%s, %s, %s, %s) \n"""%("countsTable$Diff-1",diff_gene,total_anno_gene-diff_gene,"countsTable$All")+
        """ countsTable$Q_val =  p.adjust(countsTable$pvalue, method="BH") \n""")
    #SCRIPT.write(
    #"""countsTable$qval<-qvalue(countsTable$pvalue,lambda=0)$qvalues\n""")
    #SCRIPT.write(
        #"""countsTable$qval<-qvalue(countsTable$pvalue,lambda=0)$qvalues\n""") 
    SCRIPT.write("""write.table(countsTable,row.names=FALSE,file='%s.Pathway.tsv',quote=FALSE,sep='\t')\n"""%(output))
    SCRIPT.write("resSig <-countsTable[ countsTable$qval<0.05,   ] \n")
    SCRIPT.write("""write.table(resSig,row.names=FALSE,file='%s.PathwaySig.sigend',quote=FALSE,sep='\t')\n"""%(output))
    SCRIPT.close()
    os.system("Rscript %s"%(SCRIPT.name))


def enrichment_analysis(diff_gene,total_anno_gene,sample_size,sampled_diff):
    #超几何分布检验该通路是否显著变化


    r_script = open('/tmp/phyper.%s.R' % os.getpid() ,'w')
    output = '/tmp/phyper.%s.dat' % os.getpid()
    r_script.write( 'result<- 1- phyper(%s, %s, %s, %s)\n'%(sampled_diff-1,diff_gene,total_anno_gene-diff_gene,sample_size))
    r_script.write("write.table(result,row.names=FALSE,file='%s',quote=FALSE,sep='\t') \n"%(output))
    r_script.close()
    os.system("Rscript %s"%(r_script.name))
    output = open(output,'rU')
    p_value = float(output.read().split("\n")[1])

    os.remove(r_script.name)
    os.remove(output.name)
    return p_value

def fdr(p_value_list):    
    input_data = open('/tmp/pval.%s.txt' % os.getpid() ,'w')

    input_data.write("pval\n")
    for key in p_value_list:
        input_data.write("%s\n"%(key))
    input_data.close()
    r_script = open('/tmp/fdr_qval.%s.R' % os.getpid() ,'w')
    output ='/tmp/fdr_qval.%s.dat' % os.getpid()
    r_script.write( 
        """library(qvalue)         
pData<-read.delim( "%s", header=TRUE, stringsAsFactors=TRUE ) 

        """%(
               input_data.name,


           )


    )
    r_script.write(
        """
    pData$padj<- p.adjust(pData$pval, method="BH")
    pData$qvalue<- qvalue(pData$pval,lambda=0)$qvalues
    write.table(pData,row.names=F,file='%s',quote=FALSE,sep='\t')

    """ %(   
            output
        )
    )
    r_script.close()
    os.system("Rscript %s"%(r_script.name))
    p_adj = []
    q_qval = []
    output = open(output)
    output.next()
    for line in output:
        line_l = line.split("\t")
        p_adj.append( float(line_l[-2]) )
        q_qval.append( float(line_l[-1]) )
    os.remove(output.name)
    os.remove(r_script.name)
    os.remove(input_data.name)
    return p_adj,q_qval






def Pathway_Enrichment(output):


    enrich_result = []
    p_value_list = []

    for each_pathway in all_pathway:
        print(len( all_diff_geneinpathway) ,
                len( all_geneinpathway ),
                len( all_pathway[ each_pathway  ]  ),  
                len( diff_gene_pathway[ each_pathway  ] )
                )
        if not len( diff_gene_pathway[ each_pathway  ] ):
            continue
        if each_pathway in diff_gene_pathway:
            p_value = enrichment_analysis(
                len( all_diff_geneinpathway) ,
                len( all_geneinpathway ),
                len( all_pathway[ each_pathway  ]  ),  
                len( diff_gene_pathway[ each_pathway  ] ),


            )
            p_value_list.append(p_value)
            pathway_id,pathway_name = each_pathway.rsplit(": ",1)
            enrich_result.append(
                pathway_id+'\t'+pathway_name+'\t%s\t%s\t%s'%( 
                    len(all_pathway[ each_pathway  ]),
                    len(diff_gene_pathway[ each_pathway  ]),p_value 

                )
            )
    p_adjust ,q_adjust = fdr(p_value_list)
    padj_iter = iter(p_adjust)	
    fdr_iter  = iter(q_adjust)
    END = open(output,'w')
    END.write("ID\tName\tAll\tDiff\tP_value\tP_adjust\tQ_value\n")
    for data in enrich_result:
        qval = float(fdr_iter.next())
        padj = float(padj_iter.next())
        if qval>0.05:
            continue
        END.write(data +'\t%s\t%s\n'%(padj,qval))        


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

    RAW = open( options.Table,'rU' )
    all_pathway = Ddict()
    diff_gene_pathway = Ddict()
    all_diff_gene = File_dict(open(options.Input,'rU')).read(1,1)
    all_diff_geneinpathway = {}
    all_geneinpathway = {}
    check_path( os.path.dirname( options.output) )
    ANNO = open( options.output,'w' )
    ANNO.write(RAW.next())
    for line in RAW:
        line_l = line[:-1].split("\t")
        if not line_l[-2]:
            continue
        pathway_list  = line_l[-2].split("||")
        if line_l[0] in all_diff_gene:
            ANNO.write(line)
            for each_pathway in pathway_list:
    
                diff_gene_pathway[ each_pathway][ line_l[0] ] = ""
                all_diff_geneinpathway[ line_l[0] ] = ""
        all_geneinpathway[ line_l[0] ] = ""
            
        for each_pathway in pathway_list:    
            all_pathway[ each_pathway ][ line_l[0] ] = ""
    print(  len( all_diff_geneinpathway) )
    print( len(all_pathway) )
    Pathway_Enrichment(options.output)
