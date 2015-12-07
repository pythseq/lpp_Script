#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/6
"""
from Dependcy import *
from optparse import OptionParser

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





	(options, args) = parser.parse_args() 
	FASTA = fasta_check(open(options.input,'rU'))
	sequence = FASTA.next()[-1]
	blast_type = Nul_or_Protein(sequence)
	output_prefix = os.path.abspath(  options.output_prefix )
	out_put_path = os.path.split(output_prefix)[0]+'/'

	if not os.path.exists( out_put_path ):
		os.makedirs( out_put_path )

	diamond_result = output_prefix+'.tsv'
	error = RunDiamond(options.input,options.evalue, blast_type,"swissprot",diamond_result)
	if error:
		print( colored("%s 's Swissprot process in Diamond of eggnog is error!!","red") )
		print(colored( error,"blue"  ))
		print(  "##############################################"   )

		sys.exit()
	swiss_anno_frame = pd.read_table(  diamond_result  )	
	
	
	
	gomapping_command = "GO_Mapping.py    -i %s  -o %s"%( diamond_result,output_prefix)
	gomapping_process = subprocess.Popen( gomapping_command.split(),stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
	stdout,stderr = gomapping_process.communicate()	

	
	getGO_command = "get_GO.py  -i %(result)s.GO-mapping.detail -o   %(result)s_GO.tsv"%({ "result":output_prefix  })
	getGO_command_list = getGO_command.split()
	getGO_process = subprocess.Popen( getGO_command_list,stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
	stdout,stderr = getGO_process.communicate()	
	go_anno_frame = pd.read_table(output_prefix+"_GO.tsv")
	#merge frame
	result_data_frame = pd.DataFrame.merge( swiss_anno_frame,go_anno_frame,left_on='Name', right_on='Name', how='outer' )
	result_data_frame.to_csv("%s.xls"%(  output_prefix  ),sep="\t",index=False )
	#Draw GO
	
	golist_command = "GO_List.py -i %(out)s.GO-mapping.list -o %(out)s_GO.stats"%( {"out":output_prefix}  )
	golist_command_list = golist_command.split()
	golist_process = subprocess.Popen( golist_command_list,stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
	stdout,stderr = golist_process.communicate()	
	
	
	godraw_command = "GO_Draw.py   -i %s_GO.stats  -o %s -r %s"%(
	    output_prefix,
	    out_put_path+"stats",
	    out_put_path+'Draw.R',
	)
	cogdraw_process = subprocess.Popen(  godraw_command.split(),stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
	stdout,stderr = cogdraw_process.communicate()	
	
	






