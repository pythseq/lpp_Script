#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/8/8


from lpp import *
from  optparse import OptionParser
if __name__=='__main__':
    usage = '''usage: python2.7 %prog [options]
transfer trim overlap relationship'''
    parser = OptionParser(usage =usage )
    
    parser.add_option("-i", "--INPUT", action="store",
                      dest="inp", 
                      help="Input overlap") 
    
    
    parser.add_option("-o", "--out", action="store",
                      dest="output",
                      help="The output name you want!!") 
    
    
    
    (options, args) = parser.parse_args()
    inp = options.inp
    output = options.output
    RAW = open( inp,'rU' )
    END = open(  output,'w'   )
    for line in RAW:
        line_l = line.split('\t')
        if abs( int( line_l[0] ) - int(  line_l[1]  )        )==1:
            END.write( line   )
