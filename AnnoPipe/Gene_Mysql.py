#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/6/20
"""
from ConfigParser import ConfigParser
import os,sys
from lpp import *


from sqlobject import *
from optparse import OptionParser
class SwissProt(SQLObject):
    class sqlmeta:
        table="SwissData"
    Name = StringCol(length=400,unique=True)
    Annotation = StringCol()
    Length = IntCol()
    Name_index = DatabaseIndex(Name)



class eggNOG( SQLObject  ):
    class sqlmeta:
        table="eggNOG"
    Name = StringCol(length=400,unique=True)
    Annotation = StringCol()
    Length = IntCol()
    Name_index = DatabaseIndex(Name)
    
    
class Nr( SQLObject  ):
    class sqlmeta:
        table="Nr"
    Name = StringCol(length=400,unique=True)
    Annotation = StringCol()
    Length = IntCol()
    Name_index = DatabaseIndex(Name)
    
class KEGG( SQLObject  ):
    class sqlmeta:
        table="KEGG"
    Name = StringCol(length=400,unique=True)
    Annotation = StringCol()
    Length = IntCol()
    Name_index = DatabaseIndex(Name)
    




def get_or_create(model, **kwargs):
    ''' use it to get or create object from a table '''

    instance = model.selectBy(**kwargs)
    
    if instance.count():
        return instance
    else:
        instance = model(**kwargs)

        return instance

user = "root"
password = "gass_1985"
mysql_connection = "mysql -h 192.168.0.10 -u%s -p%s  --local-infile=1 Annotation "%(user,password)
# mysql_build = "mysql -h 192.168.0.10 -u%s -p%s  --local-infile=1 "%(user,password)
connection_string = 'mysql://%s:%s@192.168.0.10/Annotation'%(user,password)    
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

if __name__ == '__main__':
      
    
    usage = '''usage: python2.7 %prog [options] 
         parse eggNOG data
   
         '''
    parser = OptionParser(usage =usage )    
    parser.add_option("-i", "--InputData", action="store",
                      dest="Input",
                      help="NOG descripton")
     
    parser.add_option("-k", "--Kind", action="store",
                      dest="Kind",
                      help="Kind")

    (options, args) = parser.parse_args()
    

    
    
    SwissProt.createTable(ifNotExists=True)
    KEGG.createTable(ifNotExists=True)
    eggNOG.createTable(ifNotExists=True)
    Nr.createTable(ifNotExists=True)
    kind = options.Kind.lower()
    data_has = {
        "nr":Nr,
        "kegg":KEGG,
        "swissprot":SwissProt,
        "eggnog":eggNOG
    
    
    
    
    }
    if kind not in data_has:
        print(" -k must be one of %s"%(", ".join(data_has.keys())))
        sys.exit()
    table = data_has[kind]
    TMP = open("%s.tmp"%(os.getpid()) ,'w')
    for t,s in fasta_check(  open(options.Input,'rU')  ):
        t = t[1:].strip()
        length = str( len(  re.sub( "\s+","",s  )    )  )
        annotaton =t 
        name = t.split()[0]
        TMP.write(name+'\t'+annotaton+'\t'+length+'\n')
    load_rela_script = """-e 'load data local infile   "%s" into table %s (name,annotation,length);'"""%(TMP.name,table.sqlmeta.table )
    os.system(mysql_connection+load_rela_script)