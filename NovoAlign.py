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

outputpath = os.path.abspath( options.outputpath)+'/'
inputpath = os.path.abspath(  options.inputpath )+'/'
if not os.path.exists(  outputpath  ):
	os.makedirs( outputpath )
# build index
index_name = ref.rsplit(".",1)[0]

os.system( ' novoindex -k 14 -s 1 %s.ndx %s'%(  index_name,ref  )  )
cache_path = outputpath+"/cache/"
check_path( cache_path )


def BWA_MAPPING( file_list  ):
	
	name = os.path.basename(  file_list[0]   ) .split('.')[0]
	path = outputpath
	data_cache_path = cache_path+"/"+name
	check_path(data_cache_path)
	
	output_preifx = path+name
	if os.path.exists(output_preifx+".bam.bai"):
		return ""

	sorted_file = sorted(  file_list,key = lambda x:  int( re.search( 'pair(\d+)'   ,x ) .group(1)    )  )
	

	[read1_file,read2_file ]= sorted_file
	out_hash = {}
	i=0
	for a,b,c,d in fastq_check(open(read1_file) ):
		i+=1
		index = i%32
		if index not in out_hash:
			split_file1 = data_cache_path+'%i/%i.pair1'%( index,index)
			check_path(  os.path.dirname( split_file1  ))
			out_hash[i] = open(split_file1,'w')
			out_hash[i].write(a+b+c+d)
	out_hash = {}
	i=0
	for a,b,c,d in fastq_check(open(read2_file) ):
		i+=1
		index = i%32
		if index not in out_hash:
			split_file2 = data_cache_path+'%i/%i.pair2'%( index,index)
			check_path(  os.path.dirname( split_file2  ))
			out_hash[i] = open(split_file2,'w')
			out_hash[i].write(a+b+c+d)
			
	os.system("NovoAligner_Single.py  -r ../%s.ndx  -t 32 -i %s -o "%( index_name,data_cache_path,outputpath+"/"+name    )	
	
	#os.system("bwa mem  -M  -t 64  %s  %s  %s  1> %s.sam  2>/dev/null"%(ref ,read1_file,read2_file,output_preifx ))
	#os.system("samtools view  -@ 20  -bS %s.sam -o %s.bam 2>/dev/null"%( output_preifx, output_preifx ))
	#os.system("samtools sort  -@ 20  -m 10G  %s.bam    %s.sort 2>/dev/null"%( output_preifx, output_preifx ))
	os.remove( output_preifx+".bam")
	os.remove( output_preifx+".sam")
	shutil.move( output_preifx+'.sort.bam', output_preifx+'.bam')
	os.system( "samtools index   %s.bam "%(output_preifx))
	

output_hash = Ddict()
for a,b,c in os.walk(  inputpath ):
	for each_f in c:
		if re.search('.pair\d+',each_f   ):
			name = each_f.split('.')[0]
			output_hash[  name ] [  a+'/'+each_f ] = ''
input_list = []
for key in output_hash:
	input_list.append(  list(output_hash[key] ) )
print( colored(output_hash,'red' ) )
pool = multiprocessing.Pool(thread)

# map(BWA_MAPPING,input_list)
pool.map(BWA_MAPPING,input_list)
