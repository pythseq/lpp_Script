#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/8
"""
from lpp import *
from multiprocessing import Pool
from Dependcy import *

if __name__ == '__main__':
	usage = '''usage: python2.7 %prog'''
	parser = OptionParser(usage =usage ) 
	parser.add_option("-p", "--PEP", action="store", 
	                  dest="PEP", 
	                  default = "",
	                  help="protein file")
	parser.add_option("-n", "--NUL", action="store", 
                      dest="NUL", 
	                  default = "",
                      help="necleotide file")		

	parser.add_option("-o", "--end", action="store", 
                      dest="output_prefix", 
                      help="output Path")

	parser.add_option("-e", "--evalue", action="store", 
                      dest="evalue", 
                      help="evalue cutoff")	
	parser.add_option("-c", "--COG", action="store", 
		              dest="cog",
	                  default="cog",
		              help="cog kind,COG,NOG or KOG")
	(options, args) = parser.parse_args()
	pool = Pool(processes=64)
	proteinseq = options.PEP
	e_val = options.evalue
	cog = options.cog
	nuclseq = options.PEP
	data_hash1 = {}
	data_hash2 = {}
	if not options.PEP and not options.NUL:
		sys.exit()
	
	elif proteinseq:
		data_hash1 = {
		    "KEGG":proteinseq,
		    "Nr":proteinseq,
		    "COG":proteinseq,
		    "GO":proteinseq
		}
		
	elif nuclseq:
		data_hash2 = {
			"KEGG":nuclseq,
			"Nr":nuclseq,
			"COG":nuclseq,
			"GO":nuclseq,
		    "NT":nuclseq,
		}	
	data_hash2.update(data_hash1)
	data_hash = data_hash2	
	if not nuclseq:
		nuclseq = proteinseq
	elif not proteinseq:
		proteinseq = nuclseq
	
	name= os.path.basename(proteinseq).rsplit(".",1)[0]
	output_prefix = os.path.abspath(options.output_prefix)+'/Detail/'+name+'/'
	
	commandlist = [
	]
	
	for each_db in data_hash:
		if each_db =="KEGG":
			commandline = "KEGG_Annotation.py -p %(protein)s -n %(nucl)s  -o %(output_prefix)s/KEGG/ -e %(e-val)s"%( 
			    {
			        "protein":proteinseq,
			        "nucl":nuclseq,
			        "output_prefix":output_prefix,
			        "e-val":e_val
			        
			    }   
			
			)
		elif each_db == "GO":
			commandline = "GO_Annotation.py -i %(protein)s  -o %(output_prefix)s/Swiss/ -e %(e-val)s"%( 
				{
					"protein":proteinseq,
					"output_prefix":output_prefix,
					"e-val":e_val
			
				}   
			
			)		
		elif each_db == 'COG':
			commandline = "COG_Annotation.py -c %(cog)s -i %(protein)s  -o %(output_prefix)s/eggNOG/ -e %(e-val)s"%( 
				{
			        "cog":cog,
					"protein":proteinseq,
					"output_prefix":output_prefix,
					"e-val":e_val
			
				}   
			
			)			
		elif each_db =="Nr":
			commandline = " Nr_Annotation.py -i %(nucl)s  -o %(output_prefix)s/Nr/ -e %(e-val)s"%( 
			    {
			        "nucl":nuclseq,

					"output_prefix":output_prefix,
					"e-val":e_val
			
				}   
			
			)
		elif each_db =="Nt":
			commandline = " Nt_Annotation.py -i %(protein)s  -o %(output_prefix)s/Nt/ -e %(e-val)s"%( 
		        {
		            "protein":proteinseq,
		            "output_prefix":output_prefix,
		            "e-val":e_val
		
		        }   
		
		    )		
			
		commandlist.append(commandline)
		
	def run(data):
		os.system(data)
		
	print(commandlist)
	# pool.map(run,commandlist)
	
	
	