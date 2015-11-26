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
        path_name = outPATH+table_data["OrthologID"]+'/'
        if not os.path.exists(path_name):
            os.makedirs( path_name )
            
        RAW_SEQ = open(path_name+"/Unigene.fa",'w')
        RAW_SEQ.write(">"+table_data[ "H.armID" ]+'\n'+table_data[ "H.armSeq" ]+'\n'+ ">"+table_data[ "H.asID" ]+'\n'+table_data[ "H.asSeq" ]+'\n' )
        os.system("pagan --seq %s  && pagan --ref-seqfile %s/outfile.fas  --ref-treefile %s/outfile.tre  --output-ancestors"%( RAW_SEQ.name, path_name,path_name  ))
        ALL_SEQ.write(">"+table_data[ "H.armID" ]+'\n'+table_data[ "H.armSeq" ]+'\n'+ ">"+table_data[ "H.asID" ]+'\n'+table_data[ "H.asSeq" ]+'\n' )
    ALL_SEQ.close()
    os.system(  "TransDecoder  --CPU 64  -t %s"%( ALL_SEQ.name  ))
    os.system( "pagan --seq test.seq  && pagan --ref-seqfile outfile.fas  --ref-treefile outfile.tre  --output-ancestors")
    os.system("""trimal -in  YKL197C.clw  -fasta |sed -r "s/\s+[0-9]+\s+bp//g" """)