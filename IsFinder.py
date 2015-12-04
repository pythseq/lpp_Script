#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/4
"""
from lpp import *
import tempfile
import pandas as pd
from optparse import OptionParser
import poster,time,urllib2,urllib
from poster.encode import multipart_encode  
from poster.streaminghttp import register_openers 
register_openers() 
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--Sequence", action="store",
                      dest="Sequence",

                      help="Genome Sequence in fasta format")
parser.add_option("-a", "--Alignment", action="store",
                      dest="Alignment",

                      help="OutputPath")

parser.add_option("-s", "--nul", action="store",
                      dest="Nul",

                      help="Nul Seq for IS")
parser.add_option("-t", "--stat", action="store",
                  dest="STAT",

                  help="IS Staistics infomation")


if __name__ == '__main__':
	(options, args) = parser.parse_args()
	DATA = fasta_check( open(options.Sequence,'rU') )
	url = "https://www-is.biotoul.fr/blast/ncbiIS.php"
	values = {
	    "Programe":"blastn",
	    "reponse":"0",
	    "seqfile":open(options.Sequence,'rb'),
	    "seq":"",
	    "matrice":"BLOSUM62",
	    "alignement":"8"	,
	    "gapouv":	"-1",
	    "gapext":	"-1",
	    "dropoff":	"0",
	    "expect": "1e-5"	,
	    "mot":	"0",
	    "old":"1"	,
	    "nas":"1"	,
	    "thrsld":"0"	,
	    "filtre":"T",
	    "qgc":"1"	,
	    "dbgc":	"1",
	    "bhtk":	"1",
	    "elss":"0"	,
	    "bqd":	"F",
	    "pga":"T"	,
	    "match":"1"	,
	    "msmatch": "-1"	,
	    "qssad":	"3"
	}	
	datagen, headers = poster.encode.multipart_encode(values) 
	
	
	sequence = re.sub('\s+','',DATA.next()[-1])
	NUL = open(  options.Nul ,'w' )
	STAT = open( options.STAT,'w')
	STAT.write("IS_name\tNumber\tAverage.Length\n")
	is_stat = Ddict()
	data = urllib.urlencode(values)
	req = urllib2.Request(url,datagen, headers)
	response = urllib2.urlopen(req)
	try:
		uploadend = response.read()
		
		out_url = re.search("""(https[^']+)""", uploadend).group(1)
		
		result = None
		while not  result:
			time.sleep(5)
			end_output = urllib.urlopen(out_url).read()
			print(end_output)
			result = re.search("Normal view</a></font><br>(.*)</form>",end_output,re.DOTALL)
		result = result.group(1)
		
		ALN = open( options.Alignment,'w'  )
		ALN.write( '\t'.join(["Name","Ref_Source","IS_Kind","Function","Ref_Start","Ref_End","Ref_Frame","Seq_Nucl_Length","Seq_Nucleotide","IS_SeqenceIdentity","IS_AlignmentLength","IS_Mismatch","IS_GapLength","IS_QueryStart","IS_QueryEND","IS_RefStart","IS_RefEnd","IS_Evalue","IS_Bitscore"])+'\n' )
		i=0
		
		has = {}
		for line in result.split("\n")[:-1]:
			if line in has:
				continue
			has[line] = ""
			i+=1
			line_l = line.split("\t")
			chro_name = re.sub("_+$","",line_l[0].split("|")[-1])
			out_data = []
			isname= chro_name+"_IS%s"%(i)
			
			q_start,q_end = int(line_l[6]),int(line_l[7])
			if q_start <q_end:
				frame='+'
			else:
				frame='-'
				q_start,q_end  = q_end,q_start
			is_seq = sequence[q_start:q_end]
			NUL.write('>'+isname+' '+line_l[1]+'\n'+is_seq+'\n')
			is_stat[ line_l[1] ][ isname ]=is_seq
			
			is_length = len(is_seq)
			out_data.extend([isname,chro_name,"IS_Element",line_l[1],line_l[6],line_l[7],frame,str(is_length),is_seq])
			out_data.extend(line_l[2:])
			ALN.write("\t".join(out_data)+'\n')
	except Exception,error:
		print(error)
	for key in is_stat:
		STAT.write(   key+'\t%s'%( len(is_stat[key]  )   )   )
		all_length = 0
		for key2,seq2 in is_stat[ key ].items():
			all_length+= len(seq2)
			
		ave_length = all_length/len(is_stat[key] )
		STAT.write( '\t%s\n'%(  ave_length  ) )
		
		