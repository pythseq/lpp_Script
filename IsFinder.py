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

url = "https://www-is.biotoul.fr/blast/ncbiIS.php"
values = {"Programe":"blastn",
"reponse":"0",
"seq":""">1_2920314_2921899|+|1
AAAAAGCGGCAAATCATAGCGATTTGCCGCTTTCAGCTTGTCGACAAAGCCACAAAAAGT
GGCTTGATCGACAAGCTTTTTTTGTTAAAATGTGAGTGAAATCTAGTTTTTGGAGGTTTT
GCCATGTTGTCTAAGCACTCTAAAGATCAGCGCGAACAGCTTGAAGTCTTTGCCTTAAGT
GAACTTGTCCCGGAAGACCATCTGGTCAGGAAAATAGAAGAAGCCATGGACTTTTCTTTT
ATTTATGAAAAAGTTGCTCCCCTTTATTCTTCAAAAGGGCGCCCAAGCATTGATCCCGTT
GTATTGATCAAAATGGTTCTGATTCAGTACGTGTTTGGCCACCGCTCGATGCGCGAAACC
ATTAAACGGATCGAAACCGATGTCGCTTATCGCTGGTTTATTGGATATGGATTTTCTGAA
AAAATCCCTCATTTTTCAACCTTCAGTAAAAACTATGAGCGCCGTTTTCATGATACGGAC
CTATTTGAAACAATCTTCTATAAAATCTTGCGTCAGGCCATGGATCTCGGTCTTGTCGAC
CCGTCGGTCGCCTTTATCGATGGAACCCATGTCAAAGCCAATGCGAATAAGAAAAAGTTT
GTGAAGAAGATTGTGAGAAAAGAAACAAGAGCTTATCAGGAACAATTAGATCGAGAAATT
AATGCCGATCGCGAAGCCAACGGCAAAAAGCCCTTAAAGCCCAGGCAATGCTCAGAAGAA
CGGGAAATAAAAGAAAGTACGACAGATCCTGAGAGCGGTTATTTTGTAAAAGGTGAACGG
GAACGTCTTTTTGCTTATGGTTTTCATACAGCTTGTGACCGGAATGGATTTGTGCTGGGG
GCGGTTGTTGAGCCTGCCAATATTCATGACAGCCAAGTGTTCACGACCCTGTTTCAACAG
GTGAAAGAGCACGTCGCTAAGCCTCATACAGTCGCAGTTGATGCCGGATATAAAACGCCG
TTTATCGCAAAGTTTCTAAGTGATCAAAATGTCCGTCCCGTCATGCCTTACACTCGACCA
CAAACTAAAAAAGGGTTCATGAGAAAACATGAATATGTATACGATGAATATTACGATGCT
TATATTTGCCCTGACGATCACGTTCTGACATATCGCACAACCAACCGTGAAGGCTATCGG
ATTTATGCATCAGATCCAAACCGATGTGAACACTGTTCTTTTCTGAAGCAATGTACGGAA
AGTCGAAATCATCGAAAGATGATTCACAGGCATCTCTGGCAGGATCATTTGGATGAAGCC
GACCATCTTCGCCACACGGATGAGAATAGGCGAATCTACGCCAAACGCAAAGAAACGATC
GAACGAGTTTTTGCGGATTTAAAACACAAGCATGGCCTGCGCTGGACAACCCTGCGGGGA
AAGAAAAAATTGTCCATGCAGGCGATGCTTGTTTTCGCTGCCATGAATCTCAAAAAGCTG
GCGAATTGGACTTGGAAAAGTCCAATTCGCCAGCATTCTCATCGAAAAAACAGAATAAAT
TGGACAAAAATAGGTCGGATTATAAAAATCCGACCTATTTTGTCAACAGTCTGAAAGCGG
CAAATCATAGCGATTTGCCGCTTTTT""",
	
"matrice":"BLOSUM62",
"alignement":"8"	,
"gapouv":	"-1",
"gapext":	"-1",
"dropoff":	"0",
"expect": "1e-5"	,
"mot":	"0",
"old":"500"	,
"nas":"250"	,
"thrsld":"0"	,
"filtre":"T",
"qgc":"1"	,
"dbgc":	"1",
"bhtk":	"100",
"elss":"0"	,
"bqd":	"F",
"pga":"T"	,
"match":"1"	,
"msmatch": "-1"	,
"qssad":	"3"}
if __name__ == '__main__':
	(options, args) = parser.parse_args()
	DATA = fasta_check( open(options.Sequence,'rU') )
	sequence = re.sub('\s+','',DATA.next()[-1])
	NUL = open(  options.Nul ,'w' )
	data = urllib.urlencode(values)
	req = urllib2.Request(url,data)
	response = urllib2.urlopen(req)
	try:
		uploadend = response.read()
		
		out_url = re.search("""(https[^']+)""", uploadend).group(1)
		result = None
		while not  result:
			time.sleep(5)
			end_output = urllib.urlopen(out_url).read()
		
			result = re.search("Normal view</a></font><br>(.+)</form>",end_output,re.DOTALL)
		result = result.group(1)
		ALN = open( options.Alignment,'w'  )
		ALN.write( '\t'.join(["Name","Ref_Source","IS_Kind","Function","Ref_Start","Ref_End","Ref_Frame","Seq_Nucl_Length","Seq_Nucleotide","IS_SeqenceIdentity","IS_AlignmentLength","IS_Mismatch","IS_GapLength","IS_QueryStart","IS_QueryEND","IS_RefStart","IS_RefEnd","IS_Evalue","IS_Bitscore"])+'\n' )
		i=0
		for line in result.split("\n"):
			i+=1
			line_l = line.split("\t")
			out_data = []
			isname= line_l[0].split()[0]+"_IS%s"%(i)
			
			q_start,q_end = int(line_l[6]),int(line_l[7])
			if q_start <q_end:
				frame='+'
			else:
				frame='-'
				q_start,q_end  = q_end,q_start
			is_seq = sequence[q_start:q_end]
			NUL.write('>'+isname+' '+line_l[1]+'\n'+is_seq+'\n')
			is_length = len(is_seq)
			out_data.append(isname,line_l[0].split()[0],"IS_Element",line_l[1],line_l[6],line_l[7],frame,str(is_length),is_seq)
			out_data.extend(line_l[3:])
			ALN.write("\t".join(out_data)+'\n')
	except Exception,error:
		print(error)