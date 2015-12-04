#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/4
"""
from lpp import *
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
	data = urllib.urlencode(values)
	req = urllib2.Request(url,data)
	response = urllib2.urlopen(req)
	try:
		uploadend = response.read()
		out_url = re.search("""(https[^"]+)""", uploadend).group(1)
		time.sleep(5)
		end_output = urllib.urlopen(out_url).read()
		print(end_output)
		
	except:
		print(end)