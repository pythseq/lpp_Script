#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/14
"""
from lpp import *
from ConfigParser import ConfigParser
general_config = ConfigParser()
path = os.path.split(os.path.abspath(__file__))[0]+'/'
general_config.read(
    os.path.join( path+"database.ini.ini")
)
if __name__ == '__main__':

	for db, number in general_config.items("Redis"):
		print(db,number)
    
