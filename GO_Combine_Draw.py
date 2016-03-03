#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/5/4
"""

from lpp import *
END = open("cache.matrix",'w')
END.write("Sample\tTerm\tOntology\tGeneRatio\tQ_value\n")

Outputhash_name = Ddict()
sample_list = {}
for f in sys.argv[1:]:
    RAW = pd.read_table(f)

    RAW["GeneRatio"] = RAW["numDEInCat"]/RAW["numInCat"]

    new_table = pd.DataFrame(RAW,columns=["term","ontology","GeneRatio","qvalue"])
    sample_name = os.path.dirname(f).rsplit("/",1)[-1]
    for i in xrange( 0, len( new_table )  ):
        data = new_table.iloc[i]
        END.write(sample_name+'\t'+"\t".join(  [ data["term"],data["ontology"] ,str(data["GeneRatio"]),str(data["qvalue"] )] )+'\n'   )
    
 
R_CACHE = open("Draw.R",'w')
output="GO_enrichment_all.pdf"
R_CACHE.write("""
library(ggplot2)
countsTable <- read.delim( "%(inp)s", header=TRUE, stringsAsFactors=TRUE ) 
pathway_size = length(levels(factor(countsTable$Term)))
Sample_size = length(levels(factor(countsTable$Sample)))
dev.new()
pdf("%(out)s",width=3*Sample_size,height = 2*pathway_size)
qplot(data = countsTable,x=Sample,y=Term,size=GeneRatio,color=Q_value)+scale_colour_gradient(low="red", high="blue")+theme(axis.text.x=element_text(angle=45))+facet_grid(.~Ontology,scales="free_y",space="free")
dev.off()



"""%(
       {
           "inp" :END.name,
           "out": output
       }
      
   
   )
   
   
   )
os.system("Rscript %s"%(R_CACHE.name))
	
#os.remove(R_CACHE.name)
#os.remove(END.name)
