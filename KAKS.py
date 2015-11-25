#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/25
"""

from lpp import *
import pandas
from optparse import OptionParser
if __name__=="__main__":
    '# you could type [  SCRIPT_NAME  ] -h to see the help log !!!!'
    usage='''usage: python %prog [options]

    Calcite KAKS '''
    parser = OptionParser(usage =usage )

    parser.add_option("-i", "--Table", action="store",
                      dest="Table",
                      type='string',
                      help="Ortholog Table")		




    parser.add_option("-o", "--Output", action="store", 
                      dest="output_Path",
                      help="Output Path prefix")
    (options, args) = parser.parse_args()
    outPATH = os.path.abspath(options.output_Path)+'/'
    if not os.path.exists(outPATH):
        os.makedirs(outPATH)
    OrthoTable = pandas.read_table(options.Table)
    table_need = OrthoTable.loc[:,["Ortholog","H.armID","H.armSeq","H.asID","H.asSeq"]]
    Ortholog_Pair = Ddict()
    ALL_SEQ = open(outPATH+"Total.fasta",'w')
    for i in xrange(0,len(OrthoTable)):
        table_data = OrthoTable.loc[i]
        ALL_SEQ.write(">"+table_data[ "H.armID" ]+'\n'+table_data[ "H.armSeq" ]+'\n'+ ">"+table_data[ "H.asID" ]+'\n'+table_data[ "H.asSeq" ]+'\n' )
    ALL_SEQ.close()
    os.system(  "TransDecoder  --CPU 64  -t %s"%( ALL_SEQ.name  ))
        