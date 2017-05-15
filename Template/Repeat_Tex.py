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
	template = env.get_template('RepeatMasker.tex')
	END = open( InputPath+"/RepeatMasker.tex" ,'w' )

	result_dir = InputPath+"/02.RepeatMask/"
	os.system( "enscript -p %s/result.ps %s/*.tbl"%( result_dir,result_dir )   )
	os.system( "ps2pdf -p %s/result.ps %s/result.pdf"%( result_dir,result_dir )   )

	END.write(
                template.render(
                    {
	                    "Graph":"123",
                  
                }
            )
        )		
	END.close()	