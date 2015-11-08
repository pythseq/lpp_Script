#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""

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
END = open(sys.argv[2],'w')
out_title = ["Name","Sequence","Length"]
db_number = sys.argv[1]
r = redis.Redis(host='localhost',port=6379,db=int(db_number))
for key in sorted(r.hgetall("title")):
    if key not in out_title:
        out_title.append(key)
END.write("\t".join(out_title)+'\n')
cache_data = ""
for key in sorted(r.keys()):
    
    if key =="title":
        continue
    cache_data +=r.hgetall(key)[out_title[0]]

    for key2 in out_title[1:]:
        if key2 in r.hgetall(key):
            cache_data +="\t"+r.hgetall(key)[key2]

        else:
            cache_data +="\t-"

    cache_data+="\n"
        
END.write(cache_data)
        
    
	
