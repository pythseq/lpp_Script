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
	data = RAW.read()
	gene_num = len( set( re.findall("(align_\d+)", data) ) )
	
	RAW.seek(0, 0)
	r_name = ""
	intron_num = 0
	exon_length = 0
	exon_num = 0
	intron_length = 0
	for line in RAW:
		line_l = line.split("\t")
		name = re.search("(align_\d+)", line).group(1)
		start, end = int(line_l[3]), int( line_l[4]) 
		if name == r_name:
			intron_length += start - r_end
			intron_num += 1
		exon_length += end - start + 1
		exon_num += 1
		r_start, r_end = start, end
		r_name = name
	length = round( 1.0 * exon_length / exon_num)
	av_number =  round( 1.0 * exon_num / gene_num)
	av_intron =   round( 1.0 * intron_length / intron_num)
	print( "Exon length\t%s\tExon Number\t%s\tAverage Intron\t%s" % ( length, av_number, av_intron) )
