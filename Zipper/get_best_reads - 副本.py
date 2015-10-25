#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/6/14


from lpp import *
from optparse import OptionParser
def get_para(   ):
	#获得运行参数
	usage = '''
	%prog [ options ]
	'''
	parser = OptionParser( usage = usage  )


	parser.add_option("-b", "--BEST", action="store",
		              dest="best",
		              help="Location of best.edges file location")


	parser.add_option("-r","--READ",action= "store",
		              dest = "reads",
		              help=" All Hgap corrected reads file in fasta format "
		              )
	parser.add_option("-o","--OUT",action= "store",
		              dest = "output",
		              help=" Fasta file record all reads appeared in best.edges file "
		              )	

	(options, args) = parser.parse_args()
	return options,args


if __name__=='__main__':
	options,args = get_para()
	best = options.best
	reads = options.reads
	print( reads )
	output = options.output
	all_nodes = {}
	for line in open( best+'/best.edges','rU'):
		if '#' in line:
			continue
		data = []
		line_l = line[:-1].split('\t')
		all_nodes[ line_l[0]  ] = ''
		all_nodes[ line_l[2] ] = ''
		all_nodes[ line_l[4]  ] = ''
	RAW = fasta_check( open( reads,'rU' ) )
	END = open(output,'w'  )
	i=0
	for t,s in RAW:
		i+=1
		if str(i) in all_nodes:
			END.write( '>%s\n'%(i )+s )
