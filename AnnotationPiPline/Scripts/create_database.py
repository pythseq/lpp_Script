#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


db_file = os.path.abspath(sys.argv[1])
Ddatabase_engine = create_engine(  'sqlite:///%s'%(db_file) )
Ddatabase_engine.connect()
Base.metadata.create_all( Ddatabase_engine  )
Session = sessionmaker( bind = Ddatabase_engine  )
session = Session()
NUL = fasta_check(open(sys.argv[2],'rU'))
for t,s in NUL:
	try:
		t = t[1:].strip()
		name,anno = t.split(" ",1)
	except:
		continue
	go_data = get_or_create(session, AnnotationTable,Name = name)
	go_data.Function = anno
	go_data.NuSeq = re.sub("\s+","",s)
session.commit()
	
GFF = open(sys.argv[3],'rU')
for line in GFF:
	if "\tID=" not in line:
		continue
	name = re.search("\tID\=([^;]+)", line).group(1)
	source =  name.split("_")[0]
	line_l = line.split("\t")
	start,stop,frame = line_l[3],line_l[4],line_l[6]
	anno_data = get_or_create(session, AnnotationTable,Name = name)
	anno_data.Source = source
	anno_data.Start = start
	anno_data.Stop = stop
session.commit()
AA = fasta_check(open(sys.argv[4],'rU'))
for t,s in AA:
	try:
		t = t[1:].strip()
		name,anno = t.split(" ",1)
	except:
		continue
	go_data = get_or_create(session, AnnotationTable,Name = name)
	go_data.AASeq = re.sub("\s+","",s)
session.commit()

