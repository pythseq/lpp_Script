#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2017/5/12
"""
from lpp import *
from ConfigParser import ConfigParser
path =os.path.split(__file__)[0]
general_config = ConfigParser()
general_config.read(
    path+"/config.ini"
)
def Config_Parse():
	config_hash = Ddict()
	for section in general_config.sections():
		for key in general_config.options(section):

			config_hash[section][key] = general_config.get(section,key)

	return config_hash