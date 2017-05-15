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




	parser.add_option("-o", "--Output", action="store",
	                  dest="OutputPath",

	                  help="Output Path")	
		
	
	parser.add_option("-t", "--Title", action="store",
	                  dest="Title",

	                  help="Title Name")		
	
	(options, args) = parser.parse_args()
	config_hash = Config_Parse()
	OutputPath = os.path.abspath(options.OutputPath)+'/'
	Title = options.Title
	
	template_root = config_hash["Location"][  "root" ]+"/Template"
	



	templeloader = FileSystemLoader(template_root)
	env = Environment(loader = templeloader)
	template = env.get_template('Title.tex')
	END = open( OutputPath+"/Title.tex" ,'w' )
	
	END.write(
	    template.render(
	        {
	            "Title":Title,

	        }
	    )
	)	
	END.close()
	