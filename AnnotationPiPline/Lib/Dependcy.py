#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LPP --<Lpp1985@hotmail.com>
  Purpose: 
  Created: 2014/12/31
"""
import sys,os,redis
from termcolor import colored
from pyflow import WorkflowRunner
from ConfigParser import ConfigParser
from lpp import *

def Redis_trans(data_hash):
	out_data = ""
	if type(data_hash)==type(Ddict()):

		for key1 in data_hash:

			for key2,value in data_hash[key1].items():
				out_data+="""*4\r\n$4\r\nhset\r\n"""
				out_data+="$%s\r\n"%( len(key1) )
				out_data+="%s\r\n"%( key1 )
				out_data+="$%s\r\n"%( len(key2) )
				out_data+="%s\r\n"%( key2 )
				out_data+="$%s\r\n"%( len(value) )

				out_data+="%s\r\n\r\n"%( value )


	return out_data
def Get_Path( path ):
	if not os.path.exists(path):

		os.makedirs( path )
def Get_result(name):
	new_name = name.rsplit('.',1)[0]
	return new_name

# set sys.path

lib_path =  os.path.split(__file__)[0]
scripts_path = os.path.join(lib_path,"../Scripts/")

sys.path.extend([lib_path, scripts_path] )
#set Path Env
os.environ["PATH"] = os.getenv("PATH")+','+scripts_path

#parse config
config_path = os.path.join(lib_path,"../Config/")
general_config = ConfigParser()

general_config.read(
    os.path.join( config_path,"general.ini")
)
def Check_file(file_name_list):
	for key,file_name in file_name_list:
		if not os.popen("which %s"%(file_name) ).read() and not os.path.isfile(file_name):
			raise Exception(file_name +"is not exist!!!")

def Make_path(path):
	if not os.path.isdir(path):
		os.makedirs(path)


def Check_path( name,file_path):
	if not os.path.isdir(file_path):
		raise Exception(name+"'s setting--"+file_path +" is not exist!!!")
config_hash = Ddict()
def Config_Parse(general_config):
	global config_hash
	database_section = general_config.items("Database")
	util_section = general_config.items("Utils")

	for section in general_config.sections():
		for key in general_config.options(section):

			config_hash[section][key] = general_config.get(section,key)




def Get_Addtional_Config(Addtional_File):
	global config_hash
	addtional_config = ConfigParser()
	addtional_config.read(
		os.path.abspath(Addtional_File)
	)	
	for section in addtional_config.sections():
		for key in addtional_config.options(section):

			config_hash[section][key] = addtional_config.get(section,key)	



Config_Parse(general_config)
