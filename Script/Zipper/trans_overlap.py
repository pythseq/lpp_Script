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
    all_has = {}
    greedy_cache = {}
    for line in RAW:
        line_l = line.strip().split('\t')
        q_start = int( line_l[0]   )
        q_end =   int( line_l[1]   )
        s_start =  int( line_l[2]   )
        s_end =  int( line_l[3]   )
        q_aln_length = int( line_l[4]  )
        s_aln_length = int( line_l[5]  )
        q_name = int( line_l[-3]  )
        s_name = int( line_l[-2]  )
        q_length = int(line_l[7])
        s_length = int( line_l[8] )
        
        identity = line_l[6]

        if s_name - q_name   !=1:
            continue  
        q_hang = q_length-q_end
        s_hang = s_start
        if q_hang>=500:
            continue
        if s_hang>200:
            continue
        #greedy_hang = (q_hang+s_hang)/2
        END.write( '%s\t%s\tN\t%s\t%s\t%s\t%s\n'%( q_name, s_name,q_length-q_aln_length, s_length-s_aln_length,s_aln_length, identity   )  )