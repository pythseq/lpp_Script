#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/6
"""
from lpp import *
import subprocess
import os,sys
from os.path import abspath
from  termcolor import colored
import pandas as pd
def Nul_or_Protein( seq ):
	seq = re.sub("\s+","",seq.lower())
	if len(set(seq) )<7 and set(seq) & set([ 'a','t','c','g'     ]):
		blast_type="blastx"
	else:
		blast_type = "blastp"
	return blast_type

def RunDiamond( fasta,evalue,blasttype,dbname,output  ):
	if not output.endswith(".tsv"):
		output=output+".tsv"
	command = "diamond_align.py  -i %(fasta)s   -o %(output)s  -a  %(dbname)s   -e %(evalue)s -n %(dbname)s  -t %(blasttype)s"%(
	    {
	        "fasta":fasta,
	        "output":output,
	        "dbname":dbname,
	        "evalue":evalue,
	        "blasttype":blasttype
	        
	    
	    
	    }
	    
	)
	command_list = command.split()
	diamond_process = subprocess.Popen( command_list,stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
	stdout,stderr = diamond_process.communicate()
	return stderr