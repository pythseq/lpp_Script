#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2017/8/23
"""

from lpp import * 



if __name__ == '__main__':
	RAW = open(sys.argv[1], 'rU')
	exon = 0
	gene = 0
	exon_length = 0
	intron = 0
	for line in RAW:
		if line.startswith("#"):
			continue
		line_l = line.split("\t")
		if len(line_l) < 4:
			continue
		if line_l[2] == "gene":
			gene += 1
		elif line_l[2] == "exon":
			exon += 1
			length = int(line_l[4]) - int(line_l[3]) + 1
			exon_length += length
	RAW.seek(0, 0)
	t_length = 0
	for e_b in RAW.read().split("\tgene\t")[1:]:
		number = e_b.count("\texon\t") - 1
		intron += number
		d_l =  e_b.split("\t")
		length = abs(int(d_l[1]) - int(d_l[0])) + 1
		t_length += length
		
	intron_length = t_length - exon_length
	av_intron =  round( 1.0 * intron_length / intron) 
	av_number = round(1.0 *exon / gene)
	length =round( 1.0 *exon_length / exon )
	gene_length = round( 1.0*exon_length/gene  )
	print( "Gene_number\yGeneLength\tExon length\tExon Number\tAverage Intron" )
	print( "%s\t%s\t%s\t%s\t%s" % (gene,gene_length ,length, av_number, av_intron) )
		