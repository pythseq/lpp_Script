#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2016/1/12
"""

from lpp import *
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--Sequence", action="store",
                  dest="Sequence",

                  help="Genome Sequence in fasta format")
parser.add_option("-o", "--out", action="store",
                  dest="outputprefix",

                  help="outputprefix")
parser.add_option("-e", "--evalue", action="store",
                  dest="evalue",

                  help="evalue")
parser.add_option("-d", "--db", action="store",
                  dest="database",

                  help="cm database")
if __name__ == '__main__':
	(options, args) = parser.parse_args()
	database = options.database
	e_value = options.evalue
	outputprefix = options.outputprefix
	sequence  = options.Sequence
	cache_name = "/tmp/%s"%(os.getpid())
	command = "cmscan  --noali  --rfam  --acc  --cpu 64 -E %s --tblout  %s  %s %s |sort -n -k 8"%( e_value,cache_name,database,sequence )
	os.system(command)
	OUTPUT = open(  cache_name,'rU'   )
	genome_hash = {}
	GFF = open(outputprefix+".gff",'w')
	CACHE = open("cache",'w')
	for line in OUTPUT:
		CACHE.write(line)
		if line.startswith("#") or not line.strip():
			continue
		else:
			line_l = line.strip().split()
			
			if "rRNA" in line_l[0] or "tRNA" in line_l[0]:
				continue
			source = line_l[2]
			product = line_l[0]
			if source in genome_hash:
				genome_hash[source]+=1
			else:
				genome_hash[source]=1
			gene_ID = source+'.misc_RNA.TU.%s'%(genome_hash[source])
			rna_ID = source+'.misc_RNA.%s'%(genome_hash[source])
			exon_ID = source+'.misc_RNA.%s.exon1'%(genome_hash[source])
			start,end = sorted( [int(line_l[7]),int(line_l[8])] )
			frame = line_l[9]
			score = line_l[-4]
			GFF.write("%s\tInfernal\tgene\t%s\t%s\t%s\t%s\t.\tID=%s;Name=%s\n"%(
			    source,
			    start,
			    end,
			    score,
			    frame,
			    gene_ID,
			    gene_ID
			)
			          )
			GFF.write("%s\tInfernal\tmisc_RNA\t%s\t%s\t%s\t%s\t.\tID=%s;Name=%s;Parent=%s;product=%s\n"%(
				source,
				start,
				end,
				score,
				frame,
			    rna_ID,
			    rna_ID,
				gene_ID,
			    product
			)
					  )		
			GFF.write("%s\tInfernal\texon\t%s\t%s\t%s\t%s\t.\tID=%s;Name=%s;Parent=%s;product=%s\n"%(
			    source,
			    start,
			    end,
			    score,
			    frame,
			    exon_ID,
			    exon_ID,
			    rna_ID,
			    product
			)
			          )				
			
			
			