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

	gomapping_command = "GO_Mapping.py    -i %s  -o %s"%( diamond_result,cog,output_prefix)
	gomapping_process = subprocess.Popen( gomapping_command.split(),stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
	stdout,stderr = gomapping_process.communicate()	

	
	getGO_command = "get_GO.py  -i %(result)s.GO-mapping.detail -o   %(result)s.annotaion_detail"%({ "result":output_prefix  })
	getGO_command_list = getGO_command.split()
	getGO_process = subprocess.Popen( getGO_command_list,stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
	stdout,stderr = getGO_process.communicate()	
	go_anno_frame = pd.read_table(output_prefix+".annotaion_detail")
	
	
	cogdraw_command = "COG_Draw.py   -i %s.xls  -o %s -r %s"%(
	    output_prefix,
	    out_put_path+"stats",
	    out_put_path+'Draw.R',
	)
	cogdraw_process = subprocess.Popen(  cogdraw_command.split(),stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
	stdout,stderr = cogdraw_process.communicate()	






