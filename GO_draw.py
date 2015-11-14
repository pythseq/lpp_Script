#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/23
"""
import sys,os

commandline = """


#!/usr/local/bin/Rscript
require(ggplot2)
require(ggthemes)
library(grid)
exampleFile = "%s"
countsTable <- read.delim( exampleFile, header=TRUE, stringsAsFactors=TRUE )

hei<-length(levels(countsTable$term))

pdf("%s.pdf", width = 0.25*hei ,height=16)
bb <-ggplot(countsTable,aes(term,numDEInCat))
aa<-bb+facet_grid(.~ontology,scales="free_x",space="free")+scale_y_continuous(trans='log')+theme_few()+geom_bar(aes(fill=ontology,position="dodge",order=numDEInCat),stat="identity")+theme(legend.position="none",axis.text.x=element_text(angle=75,hjust=1.0,size=12),axis.title.y = element_text(size = 18),strip.text.x = element_text(size=30,color="darkred",face="bold")  )+ylab("Gene Number")


dev.off()


"""%(sys.argv[1],sys.argv[2])
SCRIPT = open(sys.argv[3],'w')
SCRIPT.write(commandline)
SCRIPT.close()
os.system("Rscript %s"%(sys.argv[3]))
