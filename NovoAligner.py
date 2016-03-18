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



parser.add_option("-i", "--input", action="store", 
                  dest="inputpath",
                  type='string',
                  help="input path")

(options, args) = parser.parse_args() 
ref = options.ref
thread = options.thread

inputpath = os.path.abspath(  options.inputpath )+'/'

# build index
index_name = ref.rsplit(".",1)[0]




def Mapping( file_list  ):

    name = os.path.basename(  file_list[0]   ) .split('.')[0]


    output_preifx = path+name
    if os.path.exists(output_preifx+".bam.bai"):
        return ""

    sorted_file = sorted(  file_list,key = lambda x:  int( re.search( 'pair(\d+)'   ,x ) .group(1)    )  )


    [read1_file,read2_file ]= sorted_file
    outprefix =   read1_file.rsplit(".",1)[0]
    os.system(" novoalign -­f %s %s ­-d%s  "%( read1_file, read2_file,  index_name  )  )

    os.system("samtools view  -@ 20  -bS %s.sam -o %s.bam 2>/dev/null"%( output_preifx, output_preifx ))
    #os.system("samtools sort  -@ 20  -m 10G  %s.bam    %s.sort 2>/dev/null"%( output_preifx, output_preifx ))
    os.remove( output_preifx+".sam")



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
pool.map(Mapping,input_list)
