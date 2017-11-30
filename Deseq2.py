#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2017/11/30
"""

from lpp import *
import itertools
import os
from optparse import OptionParser
usage = '''usage: python2.7 %prog'''
parser = OptionParser(usage =usage ) 
parser.add_option("-c", "--condition", action="store", 
                  dest="Condition", 
                  default = "",
                  help="condition file")
parser.add_option("-o", "--Out", action="store", 
                  dest="OUT", 
                  default = "",
                  help="Output path")
parser.add_option("-r", "--Reads", action="store", 
                  dest="Count", 
                  default = "",
                  help="Read Count File")
parser.add_option("-t", "--Total", action="store", 
                  dest="Total", 
                  default = "",
                  help="Total output path")
(options, args) = parser.parse_args()
condition = os.path.abspath( options.Condition )
count =  os.path.abspath( options.Count )
outputpath = os.path.abspath( options.OUT )
totalpath = os.path.abspath( options.Total )
if not os.path.exists(totalpath):
	os.makedirs(totalpath)
condition_type = {}
RAW = open( options.Condition, 'rU')
RAW.next()
for line in RAW:
	line_l = line.split("\t")
	condition_type[line_l[1]] = ""
	
if __name__ == '__main__':
	
	for c1, c2 in  itertools.combinations(condition_type, 2):
		prefix_path = outputpath + '/%s__%s' % (c1, c2)
		if not os.path.exists(prefix_path):
			os.makedirs(prefix_path)
		prefix =  prefix_path + '/%s__%s' % (c1, c2)
		RFILE = open(prefix_path + '/Deseq.R', 'w')
		rscript = """
		
library("DESeq2")
library("BiocParallel")
require(ggplot2)
require(ggthemes)
library("RColorBrewer")
library('pheatmap')
register(MulticoreParam(32))
condFile = "{condition}"
coldata <- read.delim( condFile, header=TRUE, row.names="Sample",stringsAsFactors=TRUE )
coldata <- coldata[coldata$condition %in% c("{c1}","{c2}"),]
exampleFile = "{count}"
cts <- read.delim( exampleFile, header=TRUE, stringsAsFactors=TRUE, row.names=1  ) 
cts<- cts[,rownames(coldata)]
dds <- DESeqDataSetFromMatrix(countData = cts,
                              colData = coldata,
                              design = ~ condition)
dds <- dds[ rowSums(counts(dds)) > 1, ]
dds$condition <- factor(dds$condition, levels=c("{c1}","{c2}"))
dds <- DESeq(dds,parallel=TRUE)
res <- results(dds, alpha=0.05,parallel=TRUE,lfcThreshold = 1)
resOrdered <- res[order(res$padj),]
summary(resOrdered)
resSig <- subset(resOrdered, padj < 0.05)
resSig$id<- rownames(resSig)
resSigUp <- subset(resSig, log2FoldChange>0)
resSigDown <- subset(resSig, log2FoldChange<0)

		  
write.table(as.data.frame(resSig), 
         file="{prefix}.end",quote=FALSE,sep='\t',row.names=FALSE)
write.table(as.data.frame(resSigUp), 
         file="{prefix}_up.end",quote=FALSE,sep='\t',row.names=FALSE)
write.table(as.data.frame(resSigDown), 
         file="{prefix}_down.end",quote=FALSE,sep='\t',row.names=FALSE)

#How many adjusted p-values were less than 0.1?
sum(res$padj < 0.05, na.rm=TRUE) 

sum(res$padj < 0.05, na.rm=TRUE)
summary(res)
#差异基因数目统计 fdr<0.5 log2FoldChange >1
summary(resSig)


#画basemean-FC图
res$Condition = cbind(rep("Not DEGs",nrow(res)))
res$Condition[res$log2FoldChange>0 & res$padj < 0.05   ]<-"Up regulated gene"
res$Condition[res$log2FoldChange<0 & res$padj < 0.05  ]<-"Down regulated gene"
pdf(file='{prefix}.basemean-logFC-Diff.pdf')
ggplot(as.data.frame(res),aes(log2(baseMean),log2FoldChange,col=Condition))+geom_point()+ylab("log2FoldChange")+theme_few()+xlab("baseMean")+ggtitle("{title} Diff")+scale_colour_manual(values=c("green", "blue", "red"))+ geom_hline(yintercept=0,col="red")+ guides(colour = guide_legend(title = "FDR<0.05 and |log2Foldchange|>=1"))+theme(legend.position=c(.2, .9))+xlim(-2,max(log2(res$baseMean))+1)
dev.off()
#画火山图
pdf(file='{prefix}.Volcano-Diff.pdf')
ggplot(as.data.frame(res),aes(log2FoldChange,-log10(padj),col=Condition))+geom_point()+ylab("-log10(FDR)")+theme_few()+xlab("log2FC")+ggtitle("{title} Volcano plot")+scale_colour_manual(values=c("green", "blue", "red"))+ geom_hline(yintercept=0,col="red")+ guides(colour = guide_legend(title = "FDR<0.05 and |log2Foldchange|>=1"))+theme(legend.position=c(.2, .9))
dev.off()

############聚类分析，首先对表达count进行标准化处理，之后进行聚类**这一步时间较长
rld <- rlog(dds, blind=FALSE)
###############样本聚类图
sampleDists <- dist(t(assay(rld)))
sampleDistMatrix <- as.matrix(sampleDists)
rownames(sampleDistMatrix) <- paste(rld$condition, sep="-")
colnames(sampleDistMatrix) <- colnames(rld)
colors <- colorRampPalette( rev(brewer.pal(9, "Blues")) )(255)
pheatmap(sampleDistMatrix,
         clustering_distance_rows=sampleDists,
         clustering_distance_cols=sampleDists,
         col=colors,cellwidth = 15, cellheight = 12, fontsize = 8,filename = "{prefix}.clustering_sample.pdf")
#############PCA##############
pdf(file="{prefix}.PCA.pdf")
plotPCA(rld, intgroup=c("condition"))
dev.off()
############差异基因聚类分析##################
a=assay(rld) #数据格式转化
diff=a[rownames(resSig),] #提取差异基因的表达值
colnames(diff) <- paste(colnames(diff),rld$condition, sep="-")
pheatmap(diff,filename='{prefix}.diff_cluster.pdf',show_rownames=F) #聚类画图 默认采用欧式距离进行聚类
####################MA图######################################
pdf(file="{prefix}.MA.pdf")
plotMA(res, ylim=c(-10,10))
dev.off()
######样本表达盒状图#####################
n.sample=ncol(a)
if(n.sample>40) par(cex = 0.5)
cols <- rainbow(n.sample*1.2)
pdf(file='{prefix}.expression_value-box.pdf')
boxplot(a,col = cols, main="expression value",las=2)
dev.off()
##############################################

	
	
	
	""".format (
		   condition=condition,
		   prefix = prefix,
		   count = count,
		   c1 = c1,
		   c2 = c2,
		   title = c1+" vs "+c2
		   
	       
	   )
		RFILE.write(rscript)
		RFILE.close()
		os.system(" Rscript %s"%(RFILE.name))
	total = """

library("DESeq2")
library("BiocParallel")
require(ggplot2)
require(ggthemes)
library("RColorBrewer")
library('pheatmap')
register(MulticoreParam(32))
condFile = "{condition}"
coldata <- read.delim( condFile, header=TRUE, row.names="Sample",stringsAsFactors=TRUE )

exampleFile = "{count}"
cts <- read.delim( exampleFile, header=TRUE, stringsAsFactors=TRUE, row.names=1  ) 
cts<- cts[,rownames(coldata)]
dds <- DESeqDataSetFromMatrix(countData = cts,
                              colData = coldata,
                              design = ~ condition)
dds <- dds[ rowSums(counts(dds)) > 1, ]


############聚类分析，首先对表达count进行标准化处理，之后进行聚类**这一步时间较长
rld <- rlog(dds, blind=FALSE)
###############样本聚类图
sampleDists <- dist(t(assay(rld)))
sampleDistMatrix <- as.matrix(sampleDists)
rownames(sampleDistMatrix) <- paste(rld$condition, sep="-")
colnames(sampleDistMatrix) <- colnames(rld)
colors <- colorRampPalette( rev(brewer.pal(9, "Blues")) )(255)
pheatmap(sampleDistMatrix,
         clustering_distance_rows=sampleDists,
         clustering_distance_cols=sampleDists,
         col=colors,cellwidth = 15, cellheight = 12, fontsize = 8,filename = "{prefix}.clustering_sample.pdf")
#############PCA##############
pdf(file="{prefix}.PCA.pdf")
plotPCA(rld, intgroup=c("condition"))
dev.off()
######样本表达盒状图#####################
a=assay(rld)
n.sample=ncol(a)
if(n.sample>40) par(cex = 0.5)
cols <- rainbow(n.sample*1.2)
pdf(file='{prefix}.expression_value-box.pdf')
boxplot(a,col = cols, main="expression value",las=2)
dev.off()
	
	
	""".format (
	       
	    condition=condition,
	    prefix = totalpath + '/Total', 
	    count = count,

      
	)
	END = open("%s/Total.R"%(totalpath), 'w')
	END.write(total)
	END.close()
	os.system(" Rscript %s"%(END.name))
