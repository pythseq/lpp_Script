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
def Run(data):
	os.system(data)
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
	nuclseq = options.NUL
	data_hash1 = {}
	data_hash2 = {}
	if not options.PEP and not options.NUL:
		sys.exit()
	
	if proteinseq:
		data_hash1 = {
		    "KEGG":proteinseq,
		    "Nr":proteinseq,
		    "COG":proteinseq,
		    "GO":proteinseq
		}
		
	if nuclseq:
		data_hash2 = {
			"KEGG":nuclseq,
			"Nr":nuclseq,
			"COG":nuclseq,
			"GO":nuclseq,
		    "Nt":nuclseq,
		}	
	data_hash2.update(data_hash1)
	data_hash = data_hash2	
	if not nuclseq:
		nuclseq = proteinseq
	elif not proteinseq:
		proteinseq = nuclseq
	
	name= os.path.basename(proteinseq).rsplit(".",1)[0]
	output_prefix = os.path.abspath(options.output_prefix)+'/Detail/'+name+'/'
	proteinseq = os.path.abspath(proteinseq)
	nuclseq = os.path.abspath(nuclseq)
	commandlist = [
	]
	
	for each_db in data_hash:
		if each_db =="KEGG":
			commandline = "KEGG_Annotation.py -p %(protein)s -n %(nucl)s  -o %(output_prefix)s/KEGG/%(name)s -e %(e-val)s"%( 
			    {
			        "name":name,
			        "protein":proteinseq,
			        "nucl":nuclseq,
			        "output_prefix":output_prefix,
			        "e-val":e_val
			        
			    }   
			
			)
		elif each_db == "GO":
			commandline = "GO_Annotation.py -i %(protein)s  -o %(output_prefix)s/Swiss/%(name)s -e %(e-val)s"%( 
				{
			        "name":name,
					"protein":proteinseq,
					"output_prefix":output_prefix,
					"e-val":e_val
			
				}   
			
			)		
		elif each_db == 'COG':
			commandline = "COG_Annotation.py -c %(cog)s -i %(protein)s  -o %(output_prefix)s/eggNOG/%(name)s -e %(e-val)s"%( 
				{
			        "name":name,
			        "cog":cog,
					"protein":proteinseq,
					"output_prefix":output_prefix,
					"e-val":e_val
			
				}   
			
			)			
		elif each_db =="Nr":
			commandline = " Nr_Annotation.py -i %(protein)s  -o %(output_prefix)s/Nr/%(name)s -e %(e-val)s"%( 
			    {
			        "name":name,
			        "protein":proteinseq,
					"output_prefix":output_prefix,
					"e-val":e_val
			
				}   
			
			)
		elif each_db =="Nt":
			commandline = " Nt_Annotation.py -i %(nucl)s  -o %(output_prefix)s/Nt/%(name)s -e %(e-val)s"%( 
		        {
			        "name":name,
		            "nucl":nuclseq,
		            "output_prefix":output_prefix,
		            "e-val":e_val
		
		        }   
		
		    )		
			
		commandlist.append(commandline)
		
	
		
	# print('\n'.join(commandlist))
	pool.map(Run,commandlist)
	
	
	