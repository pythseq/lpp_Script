#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys,redis
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from  optparse import OptionParser
from Dependcy import *
if __name__=="__main__":
	
	usage='''usage: python %prog [options]
	It can automaticaly analysis RPKM and plot it'''
	
	parser = OptionParser(usage =usage )
	parser.add_option("-d", "--Dbnumber", action="store",
		              dest="dbnum",
		              type='int',
		              help="input fastq file")

	
	parser.add_option("-f", "--fasta_file", action="store",
		              dest="fasta",
		              type='string',
	
		              help="unigene fasta ")
	parser.add_option("-m", "--Matrix_file", action="store",
		              dest="matrix",
		              type='string',
	
		              help="reads mapping tpm")
	parser.add_option("-c", "--Count", action="store",
		              dest="count",
		              type='string',
	
		              help="reads mapping number")	
	
	
	parser.add_option("-o", "--OUTPUT", action="store",
		              dest="output",
		              type='string',
	
		              help="Output prefix")
	parser.add_option("-g", "--Graph", action="store",
		              dest="graph",
		              type='string',
	
		              help="RPKM graph  output")
	parser.add_option("-t", "--Threshold", action="store",
	                  dest="threshold",
	                  type='float',

	                  help="Filter Threshold of tpm")	
	
	
	(options, args) = parser.parse_args()	
	db_number = options.dbnum
	r = redis.Redis(host='localhost',port=6379,db=db_number)
	r.flushall()
	FB_FILE = open(options.output+".redis",'w')
	FASTA = fasta_check(  open(options.fasta,'rU')  )
	seq_length = {}
	seq_data = {}
	for t,s in FASTA:
		name = t.split()[0][1:]
		s = re.sub("\s+", '', s)
		seq_length[name] = len(s)
		seq_data[name] = s
	MATRIX = open(options.matrix,'rU')
	title = MATRIX.next()
	title_l = title.strip().split("\t")
	data_hash = Ddict()
	CACHE=open("TPM.cache",'w')
	VALIDATE=open(options.output+".tpm",'w')
	BED = open(options.output+".bed",'w')
	
	VALIDATE.write(title)
	CACHE.write("TPM\tSample")
	for key in title_l[1:]:
		CACHE.write("\t"+key)
	
	CACHE.write("\n")
	
	
	all_has = {}
	END_FASTA = open(options.output+'.fa','w')
	
	for line in MATRIX:
		line_l = line[:-1].split("\t")
		name = line_l[0]
		rpkm_data = map(lambda x:float(x)  ,line_l[1:])
		has = filter(lambda x: x>=options.threshold,rpkm_data)
		if has:
			all_has[name]=""
			END_FASTA.write('>'+name+'\n'+seq_data[name]+'\n')
			data_hash[name]["Sequence"] = seq_data[name]
			data_hash[name]["Sequence_Length"] = str(len(seq_data[name]))
			
			bed_cache = [ line_l[0],"0",str(seq_length[ line_l[0] ]-1),line_l[0],"0","+","0",str(seq_length[ line_l[0] ]-1),"0","1" , str(seq_length[ line_l[0] ]),"0" ]
			BED.write('\t'.join(bed_cache)+'\n')
			VALIDATE.write(line)
			for i in xrange(1,len(line_l)):
				
				data_hash[name]["RPKM_"+title_l[i]]=line_l[i]
				CACHE.write(line_l[i]+'\t'+title_l[i]+'\n')
	COUNT = open(options.count,'rU')
	END_COUNT = open(options.output+".count",'w')
	END_COUNT.write(COUNT.next())
	for line in COUNT:
		line_l = line.split("\t")
		if line_l[0] in all_has:
			END_COUNT.write(line)
			for i in xrange(1,len(line_l)):
			
				data_hash[name]["COUNT_"+title_l[i]]=line_l[i]

		
	for data in data_hash[name]:
		data_hash["title"][data] = ""	
	R = open("RPKM.Rscript",'w')
	R.write("""
	library("ggplot2")
	countsTable <- read.delim( "%s", header=TRUE, stringsAsFactors=TRUE )
	pdf("%s.pdf")
	ggplot(countsTable, aes(log10(TPM+1),fill=Sample))+geom_density(alpha=0.2) 
	dev.off()
	
	
	"""%(CACHE.name,options.graph))
	R.close()
	os.system("Rscript %s"%(R.name))
				
	FB_FILE.write(Redis_trans(data_hash))