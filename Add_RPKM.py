#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
from lpp import *
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-o", "--Output", action="store",
                  dest="OutputPrefix",

                  help="OutputPrefix")
parser.add_option("-t", "--Threshold", action="store",
                  dest="Threshold",
                  type="float",

                  help="rpkm threshold")

parser.add_option("-S", "--Fasta", action="store",
                  dest="Seq",

                  help="Sequence File")

parser.add_option("-r", "--Rpkm", action="store",
                  dest="Rpkm",

                  help="Rpkm File")
if __name__ == '__main__':
	(options, args) = parser.parse_args()
	thrshold = options.Threshold
	rpkm_data= pd.read_table(options.rpkm)
	rpkm_data["max"] = data[ data.columns[1:]   ].max(1)
	rpkm_filter = rpkm_data[  rpkm_data["max"] >=thrshold   ]
	rpkm_filter.to_csv(options.OutputPrefix+'.rpkm',index = False,sep = "\t"   )
	all_filteredGene = list(rpkm_data["gene"])
	fil_geneHash =  zip(all_filteredGene,[""]*len(all_filteredGene))
	TMP = open("%s.tmp"%os.getpid(),'w')
	TMP.write("gene\tSequence\n")
	SEQ = open(   optios.OutputPrefix+'.fasta','w'    )
	BED = open(   optios.OutputPrefix+'.bed','w'    )
	for t,s in fasta_check(  open( options.Seq  )  ):
		name  = t[1:].split()[0]
		s1 = re.sub( "\s+", '', s )
		if name in fil_geneHash:
			TMP.write(name+'\t'+s1+'\n')
			SEQ.write(t+s)
			BED.write(
			 '\t'.join(
			    [
			        name,
			        "0",
			        str( len(s1)  ),
			        name,
			        '0',
			        '+',
			        '0',
			        str( len(s1)  ),
			        '0',
			        '1',
			        str( len(s1)+1  ),
			        '0'
			        
			    
			    
			    
			    ]
			 
			 
			 
			 )   +'\n'
			
			
			
			)
	TMP.close()
	seq_data = pd.read_table( TMP.name  )
	tsv_data = pd.DataFrame.merge( seq_data,rpkm_data,on="gene",how="left"   )
	tsv_data.to_csv( options.OutputPrefix+'.xls',sep='\t',index=False)
	