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
NR_ANNO_DETAIL = open(sys.argv[2],'rU')
for line in NR_ANNO_DETAIL:
	line_l = line[:-1].split("\t")
	go_data = get_or_create(session,AnnotationTable_RPKM,Name = line_l[0].split()[0])
	go_data.Nr_Hit = line_l[1]+" "+line_l[6]
	go_data.Nr_Eval = line_l[-2]
	go_data.Nr_Identity = line_l[2]
	go_data.Nr_BitScore = line_l[-1]
	session.commit()

