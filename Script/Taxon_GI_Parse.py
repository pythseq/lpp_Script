#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/6/9
"""


from lpp import *
from collections import namedtuple

from sqlobject import *
from optparse import OptionParser
user = "root"
password = "gass_1985"
mysql_connection = "mysql -u%s -p%s  --local-infile=1 Taxon "%(user,password)
mysql_build = "mysql -u%s -p%s  --local-infile=1 "%(user,password)
connection_string = 'mysql://%s:%s@localhost/Taxon'%(user,password)    
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection
class Taxon_GI(SQLObject):
    class sqlmeta:
        table="GI_Taxon"
    GI = IntCol (length=50,unique=True)
    Taxon = IntCol (length=50)
    
    taxon_index= DatabaseIndex(Taxon)
    gi_index= DatabaseIndex(GI)
    
class Taxon_Classification(SQLObject):
    class sqlmeta:
        table="Taxon_Class"
    Taxon = IntCol (length=50,unique=True)
    Class = StringCol(length=50,unique=False)
    taxon_index= DatabaseIndex(Taxon)
    class_index =  DatabaseIndex(Class)
    
def get_or_create(model, **kwargs):
    ''' use it to get or create object from a table '''

    instance = model.selectBy(**kwargs)
    
    if instance.count():
        return instance
    else:
        instance = model(**kwargs)

        return instance
if __name__ == '__main__':
    usage = '''usage: python2.7 %prog [options] 
         parse eggNOG data
   
         '''
    parser = OptionParser(usage =usage )    
    parser.add_option("-T", "--GI", action="store",
                      dest="gi_taxon",
                      help="gi_taxon mapping infomation")
    parser.add_option("-c", "--Class", action="store",
                      dest="classfi",
                      help="Taxon classfi")
   
    
    (options, args) = parser.parse_args()
    os.system(mysql_build+"-e 'create database Taxon;'")
    os.system(mysql_build+"-e 'drop database Taxon;'")
    os.system(mysql_build+"-e 'create database Taxon;'")
    Taxon_GI.createTable(ifNotExists=True)
    Taxon_Classification.createTable(ifNotExists=True)
    load_des_script = """-e 'load data local infile   "%s" into table GI_Taxon (g_i, taxon);'"""%(options.gi_taxon)
    os.system( mysql_connection+load_des_script   )    
    
    load_des_script = """-e 'load data local infile   "%s" into table Taxon_Class ( taxon,class );'"""%(options.classfi)
    os.system( mysql_connection+load_des_script   )    
    
