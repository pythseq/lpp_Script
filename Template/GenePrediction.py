#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/11/12
"""


from lpp import *
import os
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
	template = env.get_template('GenePrediction.py')
	END = open( InputPath+"GenePrediction.py" ,'w' )

	result_dir = InputPath+"10.CircleGraph/"
	all_graph = []
	for each_f in glob.glob(result_dir+'/*.png'):
		name = os.path.basename( each_f).split(".")[0].split("_")[-1]
		tex = each_f.replce("png","tex")
		os.system( """' Graph2tex.py  -i %s  -o %s -c "%s基因组视图"  """%(    
		    each_f,each_f.replce("png","tex"),name
		) 
		           
		        )
		all_graph.append(  tex )
	
	total_dir = InputPath+"09.AllResult/"
	os.system(  "" )	
	