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
    parser.add_option("-r", "--reads", action="store",
                          dest="reads",
                          help="The reads in fasta format!!")     
    
    
    (options, args) = parser.parse_args()
    inp = options.inp
    output = options.output
    reads = options.reads
    RAW = open( inp,'rU' )
    END = open(  output,'w'   )
    all_reads = {}
    READS = fasta_check( open( reads,'rU'    ) )
    for t,s in READS:
        t = t[1:-1]
        s = re.sub( '\s+','',s )
        all_reads[t] = s

    assembly_out = all_reads['1']
    has = {}
    all_align =filter(  lambda x: x, RAW.read().split('\n')  ) 
    print( all_align )
    all_align = sorted( all_align,key = lambda x: int( x.split('\t')[0] ))
    
    for line in all_align:
        line_l = line.strip().split('\t')
        has[ line_l[0] ] = ''
        has[  line_l[1]  ] = ''
        enlongation_candid = line_l[1]
        b_hang = all_reads[ enlongation_candid  ][-int( line_l[-3] ):]
        
        assembly_out+=b_hang
    for i in all_reads:
        if i not in has:
            os.system( 'echo \'%s %s\' >>123'%( i,reads )  )
    assembly_out = re.sub( '(\S{60})','\\1\n',assembly_out  )
    END.write( '>END\n'+assembly_out +'\n' )