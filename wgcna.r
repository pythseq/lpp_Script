ALLOW_WGCNA_THREADS=64
library(WGCNA);
options(stringsAsFactors = FALSE)
library("corrplot")
enableWGCNAThreads()
###Data Prepare
Args <- commandArgs()
path <- getwd(  )
setwd(path)

if (! file.exists("Module")){
	dir.create("Module")
	}
datExpr = read.delim(Args[6],sep = "\t",header=T, row.names=1)
datExpr = log2(datExpr+1)
datExpr = as.data.frame(t(datExpr))
gsg = goodSamplesGenes(datExpr, verbose = 3)
if( !gsg$allOK ){
  datExpr = datExpr[gsg$goodSamples, gsg$goodGenes]
}

###Find Outlier Group
pdf("Outlier.pdf",width = 12, height = 9)
sampleTree = hclust(dist(datExpr), method = "average")
par(mar = c(0,4,2,0))
plot(sampleTree, main = "Sample clustering to detect outliers", sub="", xlab="", cex.lab = 1.5,
cex.axis = 1.5, cex.main = 2)
abline(h = 15, col = "red")
dev.off()
#clust = cutreeStatic(sampleTree, cutHeight = Args[7], minSize = 10)

#keepSamples = (clust==1)
#datExpr = datExpr[keepSamples, ]




###Calculate Mean
meanExpressionByArray=apply( datExpr,1,mean, na.rm=T)
NumberMissingByArray=apply( is.na(data.frame(datExpr)),1, sum)
KeepArray= NumberMissingByArray<500



###Keep Gene Has bigger variance and most sample present
#remove gene has most of 0 or is None
no.presentdatExp =as.vector(apply( data.frame(datExpr)==0 |is.na(data.frame(datExpr)) ,2, sum) )

variancedatExpr= as.vector(apply(as.matrix(datExpr),2,var, na.rm=T))

KeepGenes= variancedatExpr>0 & no.presentdatExp>4
datExpr=datExpr[ ,KeepGenes]


pdf("SampleMean.pdf")

barplot(
	meanExpressionByArray,
	xlab = "Sample", 
	ylab = "Mean expression",
	main ="Mean expression across samples",
	 cex.names = 0.7)
dev.off()
beta1 = 7
Connectivity=softConnectivity(datExpr,power=beta1)
ConnectivityCut = 4000
ConnectivityRank = rank(-Connectivity)
restConnectivity = ConnectivityRank <= ConnectivityCut
datExpr<-datExpr[,restConnectivity]
pdf("Exclude.pdf")
plotClusterTreeSamples(datExpr=datExpr, exclude=KeepArray)
dev.off()

pdf("R2Graph.pdf")
par(mfrow=c(1,1))
scaleFreePlot(Connectivity, main=paste("soft threshold, power=",beta1), truncated=T)
dev.off()


# number of most connected genes that will be considered
# thus our module detection uses the following number of genes


# Now we restrict the adjacency matrix to the most connected genes
ADJrest = adjacency(datExpr, power=beta1)
dissTOM=TOMdist(ADJrest)
hierTOM = hclust(as.dist(dissTOM),method="average");
pdf("GeneCluster.pdf",width=12,height=9)
#par(mfrow=c(2,1), mar=c(2,2,2,2))
#plot(hierTOM,labels=F,sub="",xlab="")


####################Static Threshold

#colorh1= cutreeStaticColor(hierTOM,cutHeight = 0.99)
#plotColorUnderTree(hierTOM,colors=data.frame(colorh1),abHeight = 0.99, )

##########Dynamic Threshold

branch.number=cutreeDynamic(hierTOM,method="tree")
colorDynamicADJ=labels2colors(branch.number )
colorh1 = colorDynamicADJ

plotDendroAndColors(hierTOM,colors=data.frame(colorh1),abHeight = 0.99, main = "Gene dendrogram and module colors")
dev.off()
pdf("Gene_VS_GeneCluster.pdf")
TOMplot(dissTOM , hierTOM, colorh1, terrainColors=TRUE)
dev.off()

##tabStaticDynamic=table(colorDynamicADJ)


datME=moduleEigengenes(datExpr,colorh1)$eigengenes
write.table(	datME,row.names=FALSE,quote=FALSE,file='PC1_module.tsv',sep="\t"	)
corr <- cor(datME)
pdf("Coor.pdf")
corrplot.mixed( corr,lower = "number", upper = "pie" )
dev.off()

pdf("Module_Cluster.pdf")
dissimME=(1-t(cor(datME, method="p")))/2
hclustdatME=hclust(as.dist(dissimME), method="average" )
plot(hclustdatME, main="Clustering tree based of the module eigengenes")
dev.off()


# Draw each Module HeatMap
TOM = TOMsimilarityFromExpr(datExpr, power = beta1)
probes<- names(datExpr)
for (name in names(datME)){
	
	which.module= substr(name ,3 ,nchar(name))
	pdf( paste(  paste("Module/",which.module,sep=""),".pdf" ,sep="" ) )
	par(mfrow=c(2,1), mar=c(0.3, 5.5, 3, 2))
	ME=datME[ , name ]
	
	plotMat(t(scale(datExpr[,colorh1==which.module ]) ),
	nrgcols=30,rlabels=F,rcols=which.module,
	main=which.module, cex.main=2)
	
	barplot(ME, col=which.module, main="", cex.main=2,
	ylab="eigengene expression",xlab="array sample")
	dev.off()
	data<-t(datExpr[,colorh1==which.module ])
	write.table(data, file=paste(  paste("Module/",which.module,sep=""),".tsv" ,sep="" ),quote=FALSE,row.names=TRUE ,sep="\t"  )
	modTOM = TOM[colorh1==which.module,colorh1==which.module]
	modProbes = probes[colorh1==which.module]
	cyt = exportNetworkToCytoscape(modTOM,
									edgeFile = paste("Module/CytoscapeInput-edges-", paste(which.module, collapse="-"), ".txt", sep=""),
									nodeFile = paste("Module/CytoscapeInput-nodes-", paste(which.module, collapse="-"), ".txt", sep=""),
									weighted = TRUE,
									threshold = 0.02,
									nodeNames = modProbes,
									altNodeNames = modProbes,
									);
}

# Read in the annotation file


