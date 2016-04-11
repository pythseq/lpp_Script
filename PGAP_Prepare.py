#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2016/4/11
"""

from lpp import *

                
                


if __name__ == '__main__':
    usage = '''usage: python2.7 %prog'''
    parser = OptionParser(usage =usage ) 
    parser.add_option("-i", "--Input", action="store", 
                      dest="Input_path", 
                      default = "",
                      help="Input_path")
    parser.add_option("-o", "--end", action="store", 
                      dest="output_path", 
                      help="output Path")
    
    (options, args) = parser.parse_args()
    input_path = options.Input_path
    output_path = options.output_path
    check_path( output_path )
    for a,b,c in os.walk(input_path):
        for e_f in c:
            if e_f=="Genome1.gbk":
                RAW = open(a+'/'+e_f)
                name = re.search( "DEFINITION.+(\S+)\.", RAW.read()).group(1)
                
    for a,b,c in os.walk(input_path):
        for e_f in c:
            if e_f=="Total.ffn":
                RAW = fasta_check( open(a+'/'+e_f) )
                END = open(output_path+'/'+name+'.nuc','w')
                for t,s in RAW:
                    END.write('>'+name+'_'+t[1:])
                    END.write(s)
            
            if e_f=="Total.faa":
                RAW = fasta_check( open(a+'/'+e_f) )
                END = open(output_path+'/'+name+'.pep','w')
                for t,s in RAW:
                    END.write('>'+name+'_'+t[1:])
                    END.write(s)  
            if os.path.exists( output_path+"/"+name+'.function' ):
                os.remove( output_path+"/"+name+'.function' )
            END = open( output_path+"/"+name+'.function','a' )        
            if e_f.endswith(".ptt"):
                RAW = open(a+'/'+e_f,'rU')
                RAW.next()
                RAW.next()
                RAW.next()
                for line in RAW:
                    line_l = line.strip().split("\t")
                    if not line_l[-2]:
                        line_l[-2]='-'
                    END.write(name+'_'+line_l[3]+'\t'+line_l[-2]+'\t'+line_l[-1]+'\n')    

