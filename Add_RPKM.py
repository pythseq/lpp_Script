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

parser.add_option("-s", "--Fasta", action="store",
                  dest="Seq",

                  help="Sequence File")

parser.add_option("-r", "--Rpkm", action="store",
                  dest="Rpkm",

                  help="Rpkm File")


parser.add_option("-c", "--Count", action="store",
                  dest="Count",

                  help="Reads Count File")
if __name__ == '__main__':
	(options, args) = parser.parse_args()
	thrshold = options.Threshold
	rpkm_data= pd.read_table(options.Rpkm)
	rpkm_data["max"] = rpkm_data[ rpkm_data.columns[1:]   ].max(1)
	rpkm_filter = rpkm_data[  rpkm_data["max"] >=thrshold   ]
	del rpkm_filter["max"]
	rpkm_filter.to_csv(options.OutputPrefix+'.rpkm',index = False,sep = "\t"   )
	old_name = rpkm_filter.columns[1:]
	new_name = [ "RPKM_"+x for x in old_name    ]
	changname_hash = dict(zip(old_name,new_name))
	rpkm_filter.rename( changname_hash, inplace=True  )
	
	all_filteredGene = list(rpkm_data["gene"])
	fil_geneHash =  dict(zip(all_filteredGene,[""]*len(all_filteredGene)))
	print(len(fil_geneHash ))
	count_data = pd.read_table( options.Count )
	count_has_data = count_data[  count_data["gene"].isin(fil_geneHash) ]	
	print(len(count_has_data))
	count_has_data.to_csv( options.OutputPrefix+'.count',sep="\t",index=False  )
	old_name = count_has_data.columns[1:]
	new_name = [ "ReadCount_"+x for x in old_name    ]
	changname_hash = dict( zip(old_name,new_name) )
	count_has_data.rename( changname_hash, inplace=True  )	
	
	TMP = open("%s.tmp"%os.getpid(),'w')
	TMP.write("gene\tSequence\n")
	SEQ = open(   options.OutputPrefix+'.fasta','w'    )
	BED = open(   options.OutputPrefix+'.bed','w'    )
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
	tsv_data = pd.DataFrame.merge( tsv_data,count_has_data,on="gene",how="left"   )
	tsv_data.to_csv( options.OutputPrefix+'.xls',sep='\t',index=False)
	os.remove(TMP.name)