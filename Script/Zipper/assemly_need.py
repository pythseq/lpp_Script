#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/8/8

from celera_zipper import libary
from lpp import *
import shutil
from configure import *
from time import time
from hashlib import md5
import subprocess
from termcolor import colored
import shlex
from  optparse import OptionParser
if __name__=='__main__':
	usage = '''usage: python2.7 %prog [options]
transfer trim overlap relationship'''
	parser = OptionParser(usage =usage )

	parser.add_option("-i", "--INPUT", action="store",
		              dest="inp", 
		              help="Input overlap") 


	parser.add_option("-o", "--out", action="store",
		              dest="output",
		              help="The output name you want!!") 

	parser.add_option("-u", "--uni", action="store",
		              dest="unitig",
		              help="Raw unitig sequence in fasta !!")

	parser.add_option("-r", "--relation", action="store",
		              dest="rela",
		              help="Raw unitig relationship")     
	
	(options, args) = parser.parse_args()
	inp = options.inp
	output = options.output
	unitig = options.unitig
	relationship = options.rela








##############################################################
##############################################################
##############################################################
	#store all sequence to a hash to prepare for output
	root_path = os.getcwd()
	all_raw_seq_hash = {}
	UNITIG = fasta_check( open( unitig,'rU' ))
	for t,s in UNITIG:
		name = t[1:-1]
		s1 = re.sub( '\s+','',s  )
		s_ = complement( s1 )
		s_ =re.sub( '(\w{60})' ,'\\1\n',s_ )
		all_raw_seq_hash[ name+'+' ] =s
		all_raw_seq_hash[ name+'-' ] =s_+'\n'


#####################################################################
#####################################################################
	#对所有的raw unitig的链接关系进行映射
	RELA = open( relationship,'rU'  )
	rela_hash = Ddict()
	for line in RELA:
		line_l = line.strip().split( '\t' )
		rela_hash[ line_l[0] ] [ '3' ] = line_l[2]
		rela_hash[ line_l[0] ] [ '5' ] = line_l[1]


######################################################################
######################################################################
######################################################################
######################################################################
	OUTPUT = open( output,'w'  )
	DETAIL = open(  output+'.detail','w'   )
	new_rela = Ddict()
#c代表contig计数器， p代表plasmid计数器
#遍历每一个out的结果，并根据生成的contig reads顺序对unitig.fasta 重新构筑结果，实用工具是minimus2，该工具被我修改，能够使用按照指定的方式将reads拼接起来

	p = 0
	c = 0
	RAW = open(  inp,'rU' )
	for line in RAW:
		line_l = line.strip().split('\t')
		if line.startswith(  'Plasmid'  ):
			#处理拼好的Plasmid
			p+=1
			OUTPUT.write(  '>Plasmid%s\n%s'%( p,all_raw_seq_hash[ line_l[1]  ]    ) )
			DETAIL.write(  'Plasmid%s\t%s\t%s\t%s\n'%( p,rela_hash[ line_l[1]     ]['5'] , rela_hash[  line_l[1]  ]['3'],'Plasmid'   )  )
		elif len(line_l)==1:
			#处理singleton

			c+=1
			OUTPUT.write(  '>Contig%s\n%s'%(c, all_raw_seq_hash[ line_l[0]  ]    ) )
			DETAIL.write(  'Contig%s\t%s\t%s\t%s\n'%( c,rela_hash[ line_l[0]     ]['5'] , rela_hash[  line_l[0]  ]['3'],'Contig'   )  )
		else:
			#处理多个unitig组成的contig
			c+=1
			if line_l[0]== line_l[-1]:
				status = 'Circled'
			else:
				status = 'Contig'
			all_have = {}
			need = []
			for each_node in line_l:
				if each_node not in all_have:
					need.append( each_node )
				all_have[ each_node ] = ''
			assembly_path = './assembly/'
			now = str( time() )
			unique = md5(now).hexdigest()
			cache_path = assembly_path+unique+'/'
			check_path(  cache_path   )
			CACHE_READS = open(    cache_path+'reads.fasta','w'  )
			for key in need:
				CACHE_READS.write( '>%s\n'%(key)+ all_raw_seq_hash[key] )
			
				
				
			subprocess.check_output( shlex.split( amos_path+'/toAmos -s %s -o %s'%(CACHE_READS.name, cache_path+'/amos.afg'    )     )   )
			minimus_command = shlex.split(  cele_path+'/minimusCE -D CONSERR=0.9 -D MINID=80 '+  cache_path+'/amos' )

			subprocess.check_output( minimus_command )

			tag='+'
			name = "Contig%s"%( c )
			s = fasta_check(  open( cache_path+'amos.fasta'  )  ).next()[-1]
			#检查拼接出来的contig是否唯一
			number = len( re.findall(  '(>)',open( cache_path+'amos.fasta'  ).read()) )
			
			if number>1:
				print( cache_path+'amos.fasta not Unique!!!!' )
			

			OUTPUT.write(  '>%s\n'%(name  )+s    )
			if tag =='+':
				DETAIL.write( '\t'.join( [ name,rela_hash[  need[0]  ]['5'] ,rela_hash[ need[-1]   ]['3'],status  ]  )+'\n'  )
			else:
				DETAIL.write( '\t'.join( [ name,rela_hash[  need[-1].translate( libary  )  ]['5'] ,rela_hash[ need[0].translate( libary  )   ]['3'],status  ]  ) +'\n' )
	shutil.rmtree( assembly_path )