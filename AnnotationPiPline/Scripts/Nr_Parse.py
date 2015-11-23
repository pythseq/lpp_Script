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
from os.path import abspath
sys.path.append( os.path.split(abspath(__file__))[0]+'/../Lib/' )
from lpp import *
from Dependcy import *

usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-d", "--Database", action="store",
                  dest="DB_FILE",

                  help="Database File")


parser.add_option("-f", "--fasta", action="store",
                  dest="fasta",
                  type='int',
                  help="database number")



if __name__ == '__main__':

    (options, args) = parser.parse_args()
    