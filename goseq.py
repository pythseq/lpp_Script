#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/6/26
"""
import sys,os
data = sys.argv[1]
length = sys.argv[3]
go = sys.argv[2]
end = sys.argv[4]
r_script="""
library("goseq")
DEG<-read.table("%(inp)s", header = FALSE)
DEG <-levels(DEG[,1])
DEG.vector <- t(DEG)
ALL<-levels(read.table("%(go)s", header = FALSE)[,1])
go <-read.table("%(go)s", header = FALSE)

ALL.vector<-c(t(ALL))
gene.vector=as.integer(ALL.vector%in%DEG.vector)
names(gene.vector)=ALL.vector 

length_info = read.table("%(length)s", header = FALSE)
gene_length.vector<-c(t(length_info[,2]))
names(gene_length.vector)<-length_info[,1]
gene_length2<-gene_length.vector[names(gene_length.vector)%in%names(gene.vector)]
pwf=nullp(gene.vector,bias.data=gene_length2,plot.fit=FALSE)
pvals <- goseq(pwf,gene2cat=go)
pvals$qvalue<-p.adjust(pvals$under_represented_pvalue, method="BH")
pvals$gene_num<-rep(length(ALL),nrow(pvals))
pvals<-pvals[c("category","numDEInCat","numInCat","under_represented_pvalue","qvalue","gene_num","term","ontology")]
colnames(pvals)[4]<-"pvalue"
pvals<-pvals[order(pvals$qvalue),]
enriched_go<-pvals[pvals$qvalue<.05,]

write.table(enriched_go,"%(out)s.go_enrich",sep="\t",row.names=FALSE,quote=FALSE)
""".replace("%(go)s",go).replace("%(inp)s",data).replace("%(length)s",length).replace("%(out)s",end)

END = open("%s.goseq.R"%(end),'w')
END.write(r_script)
END.close()

#os.system("R --no-save <  %s"%(END.name))
