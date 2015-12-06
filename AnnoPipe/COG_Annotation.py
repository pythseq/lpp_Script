#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/6
"""
from Dependcy import *


if __name__=="__main__":
	usage = '''usage: python2.7 %prog'''
	parser = OptionParser(usage =usage ) 
	parser.add_option("-i", "--INPUT", action="store", 
                  dest="input", 
                  help="input file")

	parser.add_option("-o", "--end", action="store", 
                  dest="output_prefix", 
                  help="output_prefix")
	
	parser.add_option("-e", "--evalue", action="store", 
		              dest="evalue", 
		              help="evalue cutoff")
	
	parser.add_option("-c", "--COG", action="store", 
		              dest="cog",
		              default = 'COG', 
		              help="COG,NOG or KOG")
	
	
	
	(options, args) = parser.parse_args() 
	FASTA = fasta_check(open(options.input,'rU'))
	sequence = FASTA.next()[-1]
	blast_type = Nul_or_Protein(sequence)
	