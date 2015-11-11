#!/usr/bin/python
#coding:utf-8
# Author:  LPP --<lpp1985@hotmail.com>
# Purpose: 
# Created: 2011/6/3
from lpp import *
#usage python2.7 expression_matrix_build.py     [ count.py's end__1_append_file_name  ]  [   matrix_end   ]
import glob,re,sys
from optparse import OptionParser 
usage = ''' To do Desq of Reads mapping matrix !
Usage python %prog     [Options]''' 
parser = OptionParser(usage =usage ) 
parser.add_option("-o", "--OUTPUTPATH", action="store", 
                  dest="outputpath",
                  default = 'Static_output', 
                  help="OUTPUTPATH")

parser.add_option("-a", "--append", action="store", 
                  dest="append", 
                  default = 'matrix',
                  help="Matrix of Reads number")

parser.add_option("-s", "--STATIC", action="store", 
                  dest="static_path", 

                  help="static_path of QC")

parser.add_option("-i", "--INPUT", action="store", 
                  dest="input_path", 

                  help="input path of expression")


parser.add_option("-t", "--THRESHOLD", action="store", 
                  type='float',
                  dest="threshold", 

                  help="the threshold of padj to be considered as significant!!")

(options, args) = parser.parse_args()

threshold = options.threshold

outputpath   = options.outputpath

static_path   = os.path.abspath( options.static_path )+os.sep

input_path   = options.input_path
 
append = options.append
static_path = options.static_path

if not os.path.exists(  outputpath ):
	os.makedirs( outputpath )

outputpath = os.path.abspath( outputpath  ) + os.sep

def sampleNameTrans( sample_name ):
	if re.search( '(^\d+)',sample_name  ):
		sample_name = 'X'+sample_name
	return sample_name

if not os.path.exists( static_path  ):
	print( 'ERROR!!! THE Static PATH doesn\'t exits!!!!!'  )
	sys.exit()

if not os.path.exists( input_path  ):
	print( 'ERROR!!! THE Input expression PATH doesn\'t exits!!!!!'  )
	sys.exit()
	
	



input_path = os.path.abspath(  input_path )+os.sep

# To store the total depth of Sequencing 
size_factor = {}

for each_f in glob.glob(static_path +'*.total.stats'):
	STATIC = open ( each_f ,'rU' )
	STATIC.next()
	sample_name = sampleNameTrans( os.path.split(each_f)[-1].split('.')[0] )

	size_factor[ sample_name ] = STATIC.next().split('\t')[2]
	
for each_matrix in glob.glob(  input_path+'*.'+append  ):
	stats_name = os.path.split(each_matrix)[-1].split('.')[0]
	
	sample_list = [x  for x in stats_name.split('__')]
	
	
	end_path = outputpath+stats_name
	
	if not os.path.exists(  end_path ):
		os.makedirs( end_path )
	end_path = os.path.abspath(  end_path )+os.sep
		
	matrix_output_path   = outputpath + os.path.split(  each_matrix  )[-1]+os.sep+ each_matrix+os.sep
	MATRIX = open( each_matrix,'rU'  )
	name_list = MATRIX.next()[:-1].split('\t')
	x_name = sampleNameTrans( name_list[1] )
	
	y_name = sampleNameTrans( name_list[2] )
	
	
	x_coverage = size_factor[ x_name ]
	
	y_coverage = size_factor[ y_name  ]
	
	matrix_abspath = each_matrix
	
	end_prefix = end_path + stats_name
	
	
	
	r_script = '''#!/usr/bin/Rscript
# functions

exampleFile = "%s"
countsTable <- read.delim( exampleFile, header=TRUE, stringsAsFactors=TRUE ) 

pdf(file="%s_dis.jpeg",width = 20)
par(mfrow=c(1,2) )
plot(
 countsTable$%s,
 countsTable$%s,
 xlab='%s',
 ylab='%s',
 main='%s vs %s',
 pch=20, cex=.1, 
  )

library( DESeq )

countsTable <- read.delim( exampleFile, header=TRUE, stringsAsFactors=TRUE ) 

rownames( countsTable ) <- countsTable$gene  
countsTable <- countsTable[ , -1 ]
conds <- c( "T", "N" ) 
cds <- newCountDataSet( countsTable, conds ) 
libsizes <- c(%s=%s, %s=%s)
sizeFactors(cds) <- libsizes  
cds <- estimateSizeFactors( cds ) 
cds <- estimateDispersions( cds,method='blind',sharingMode="fit-only" ,fitType="local" )   
res <- nbinomTest( cds, "T", "N" ) 

plotDE <- function( res )
 plot(
 res$baseMean,
 res$log2FoldChange,
 xlab = 'baseMean',
 ylab = 'baseMean',
 main = '%s vs %s Diff',
 
 log="x", pch=20, cex=.1,
 col = ifelse( res$padj < %s, "red", "black" ) )
 
 plotDE( res )
 dev.off()
 resSig <- res[ res$padj < %s, ]  

 write.table(resSig,row.names=FALSE,file='%s.end',quote=FALSE,sep='\t') '''%( matrix_abspath,end_prefix, x_name,y_name ,x_name,y_name ,x_name,y_name ,x_name,x_coverage,y_name,y_coverage ,y_name ,x_name,threshold,threshold, end_prefix )
	RSCRIPT = open( end_path+'Deseq.R'   ,'w' )
	RSCRIPT.write( r_script )
	RSCRIPT.close()
	os.system(  'Rscript ' +RSCRIPT.name +'&')
	
	





