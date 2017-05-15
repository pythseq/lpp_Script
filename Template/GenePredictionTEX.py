#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/11/12
"""


from lpp import *
import os,subprocess
from  jinja2 import FileSystemLoader,Environment
from Dependcy import Config_Parse
from optparse import OptionParser





if __name__ == '__main__':
	usage = '''usage: python2.7 %prog [options] 
'''
	parser = OptionParser(usage =usage )



	parser.add_option("-i", "--InputPath", action="store",
	                  dest="InputPath",

	                  help="Input Path")


	(options, args) = parser.parse_args()
	InputPath = os.path.abspath(options.InputPath)+'/'

	config_hash = Config_Parse()

	template_root = config_hash["Location"][  "root" ]+"/Template"




	templeloader = FileSystemLoader(template_root)
	env = Environment(loader = templeloader)
	template = env.get_template('GenePrediction.tex')
	END = open( InputPath+"GenePrediction.tex" ,'w' )

	result_dir = InputPath+"10.CircleGraph/"
	all_graph = []
	for each_f in glob.glob(result_dir+'/*.png'):
		name = os.path.basename( each_f).split(".")[0].split("_")[-1]
		tex = each_f.replace("png","tex")
		subprocess.call( """' Graph2tex.py  -i %s  -o %s -c %s基因组视图  """%(    
		    each_f,each_f.replace("png","tex"),name
		) .split()
		           
		        )
		print(   """' Graph2tex.py  -i %s  -o %s -c %s基因组视图  """%(    
		    each_f,each_f.replace("png","tex"),name
		)   
		         )
		all_graph.append(  tex )
	
	total_dir = InputPath+"09.AllResult/"
	os.system(  "cd %s && N50-new.py %s"%(  total_dir, "Total.ffn" )    )	
	os.system(  "cd %s && lengthN50.R %s"%(  total_dir, "Total.scope  result.pdf result.tiff" )    )	
	lengh_graph = "%s/result.pdf "%(  total_dir )                                  
	anno_path = InputPath+" 03.Annotation/"
	os.system( """txt2latex.py -i %s/stats.tsv -o %s/stats.tex   -c  "序列注释结果统计表" """%(  anno_path,anno_path  )    )    
	table = "%s/stats.tex"%( anno_path  )
	
	
	