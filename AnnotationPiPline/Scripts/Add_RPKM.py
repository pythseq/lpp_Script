#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys,redis
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import *
db_number = sys.argv[1]
r = redis.Redis(host='localhost',port=6379,db=int(db_number))
r.flushall()
FB_FILE = open(os.path.abspath(sys.argv[2]),'w')

RPKM = open(sys.argv[3],'rU')
title = RPKM.next()
title_l = title.strip().split("\t")
data_hash = Ddict()
CACHE=open("RPKM.cache",'w')
VALIDATE=open("Validate.rpkm",'w')
VALIDATE.write(title)
CACHE.write("RPKM\tSample")
for key in title_l[1:]:
	CACHE.write("\t"+key)

CACHE.write("\n")



for line in RPKM:
	line_l = line[:-1].split("\t")
	rpkm_data = map(lambda x:float(x)  ,line_l[1:])
	has = filter(lambda x: x>=1,rpkm_data)
	if has:
		VALIDATE.write(line)
		for i in xrange(1,len(line_l)):
			name = line_l[0]
			data_hash[name]["RPKM_"+title_l[i]]=line_l[i]
			CACHE.write(line_l[i]+'\t'+title_l[i]+'\n')
for data in data_hash[name]:
	data_hash["title"][data] = ""	
R = open("RPKM.Rscript",'w')
R.write("""
library("ggplot2")
countsTable <- read.delim( "%s", header=TRUE, stringsAsFactors=TRUE )
pdf("rpkm.pdf")
ggplot(countsTable, aes(log10(RPKM+1),fill=Sample))+geom_density(alpha=0.2) 
dev.off()


"""%(CACHE.name))
R.close()
os.system("Rscript %s"%(R.name))
			
FB_FILE.write(Redis_trans(data_hash))