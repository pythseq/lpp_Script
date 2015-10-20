#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/7/9

from optparse import OptionParser
from lpp import *
import subprocess,shlex
def get_para(   ):
	#获得运行参数
	usage = '''
	%prog [ options ]
	'''
	parser = OptionParser( usage = usage  )
	
	
	parser.add_option("-g", "--OVL", action="store",
		              dest="ovl",
		              help="overlapStore")
	
	parser.add_option("-q","--QUERY",action= "store",
		              dest = "query",
		              help="Query Reads ID!"
		              )
	parser.add_option("-s","--SUB",action= "store",
		                  dest = "subject",
		                  help="Subject Reads ID"
		                  )	
	(options, args) = parser.parse_args()
	return options,args
options,args = get_para()
overlstore = options.ovl
queryID = options.query
subjectID = options.subject

overlap_PATH = '/pub/SOFTWARE/Pacbio/smrtanalysis/current/analysis/bin/wgs-7.0/Linux-amd64/bin/overlapStore'

#运行overlapStore，检查两个reads是否具有overlap的结果
overlapout = subprocess.check_output(  shlex.split( overlap_PATH+' -q %s %s %s '%(  queryID,subjectID,overlstore  )    )       )
if not overlapout:
	sys.exit()

#检查是否是3‘或者5’端overlap
for direction in [ '5','3'   ]:
	output_detail = []
	command =  overlap_PATH+' -d %(overlap)s     -b %(query)s -e %(query)s -d%(tag)s | grep %(subject)s'%( 
	    {
	        'overlap':overlstore,'query':queryID,'tag':direction,'subject':subjectID }  
	)
	

	detailout = subprocess.check_output(
	    shlex.split(  command )
	)

	all_detail_block = detailout.split('\n')
	for line in all_detail_block:
		detail_block = line.split()
		if not detail_block:
			continue
		if subjectID== detail_block[1]:
			output_detail = detail_block
			break
	if output_detail:
		break
if output_detail:
	arrange = output_detail[2]
	if arrange=='N':
		read_dir = '+'
	else:
		read_dir='-'
	if direction =='3':
		print( queryID+'+'+'\t'+subjectID+read_dir      )
	else:
		print( subjectID+read_dir+'\t'+ queryID+'+'     )
