#!/usr/bin/Rscript
library("ggplot2")
require(ggthemes)
argv <- commandArgs(TRUE)

countsTable <- read.delim( argv[1], header=TRUE, stringsAsFactors=TRUE )
pdf(argv[2])
ggplot(countsTable, aes(Range,NO))+ geom_bar(alpha=0.2,stat = "identity")+ylab("Unigene Number")+theme_few()+ylab("Unigene Length")
dev.off()
tiff(argv[3])
ggplot(countsTable, aes(Range,NO))+ geom_bar(alpha=0.2,stat = "identity")+ylab("Unigene Number")+theme_few()+ylab("Unigene Length")
dev.off()
