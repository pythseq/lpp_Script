#!/usr/bin/python
#coding:utf-8
# Author:  LPP --<lpp1985@hotmail.com>
# Purpose: 
# Created: 2011/7/27
from lpp import *
import multiprocessing
from optparse import OptionParser
from termcolor import colored
usage = '''usage: python %prog [options] 

It can automaticly run BWA!!'''
parser = OptionParser(usage =usage ) 

parser.add_option("-r", "--ref", action="store", 
                  dest="ref",
                  type='string',
                  help="the reference seq")

parser.add_option("-t", "--thread", action="store", 
                  dest="thread",
                  type='int',
                  help="thread number of each BWA")

parser.add_option("-p", "--process", action="store", 
                  dest="process",
                  type='int',
                  help="process number of total BWA")

parser.add_option("-o", "--output", action="store", 
                  dest="outputpath",
                  type='string',
                  help="output path")

parser.add_option("-i", "--input", action="store", 
                  dest="inputpath",
                  type='string',
                  help="input path")

(options, args) = parser.parse_args() 
ref = options.ref
thread = options.thread
process = options.process
outputpath = options.outputpath
inputpath = os.path.abspath(  options.inputpath )
# build index
#os.system( 'bwa index -a bwtsw %s 2>&1 >/dev/null'%(  ref  )  )
def BWA_MAPPING( file_list  ):

	def get_outputname( each_f ):
		output_preifx = path+name +'.' + re.search( '(Filter\.pair\d+)$',each_f ).group(1)
		return output_preifx

		
	
	
	name = os.path.split(  file_list[0]   )  [-1] .split('.')[0]
	path = outputpath
	if path[-1] !='/':
		path = path+'/'
	output_preifx = path+name
	if not os.path.exists(  path  ):
		os.makedirs( path )
	sorted_file = sorted(  file_list,key = lambda x:  int( re.search( 'pair(\d+)'   ,x ) .group(1)    )  )
	



	os.system(  'bwa mem -T %s  -M %s %s   |samtools view -bS -|samtools sort - %s'%( thread, ref ,' '.join(sorted_file)  ,output_preifx ,   )    )

output_hash = Ddict()
for a,b,c in os.walk(  inputpath ):
	for each_f in c:
		if re.search('Filter.pair\d+',each_f   ):
			name = each_f.split('.')[0]
			output_hash[  name ] [  a+'/'+each_f ] = ''
out_list = []
print( colored(output_hash,'red' ) )
for each_data in output_hash:
	out_list.append( list(  output_hash[  each_data ]  )  )
all_process = []
while out_list:
	if len( multiprocessing.process.active_children() )< process:
		print(out_list)
		BWAprocess = multiprocessing.Process( target = BWA_MAPPING,args=(   out_list.pop() ,)  )
		BWAprocess.daemon = False
		BWAprocess.start()
		all_process.append( BWAprocess )
		
for each_process in all_process:
	each_process.join()
