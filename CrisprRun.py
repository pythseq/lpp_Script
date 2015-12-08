#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/8
"""
from lpp import *

import pandas as pd
if __name__ == '__main__':
    usage = '''usage: python2.7 %prog [options] 
		     Pilr-CR Crispr Finding !!!
		     '''
    
    parser = OptionParser(usage =usage )    
    parser.add_option("-g", "--Genome", action="store",
                      dest="Genome",
                      help="Genome Sequence")


    parser.add_option("-o", "--OUTPUT", action="store",
                      dest="outputprefix",
                      help="Output Path") 

    (options, args) = parser.parse_args()
    outputprefix = options.outputprefix
    output_path = check_path(os.path.dirname(outputprefix) )    
    
    Genome = os.path.abspath(options.Genome)
    TMP_INPUT = open( output_path+"%s.contigs"%(os.getpid()),'w' )
    seq_hash = {}
    for t,s in fasta_check( open(Genome,'rU') ):
        t = re.sub( "_+$","", t.strip().split("|")[-1])
        if t.startswith('>'):
            t = t[1:]
            
        s1 = re.sub("\s+", "", s)
        seq_hash[t]=s1
        TMP_INPUT.write('>'+t+'\n'+s)
        
    TMP_INPUT.close()
        
    
    tmp_name = output_path+"%s.tmp"%(os.getpid())
    os.system ("pilercr -in %s  -out %s -seq %s_DP.fa -quiet -noinfo -trimseqs"%(TMP_INPUT.name,tmp_name,outputprefix))
    os.remove( TMP_INPUT.name)
    
    RAW = open(tmp_name,'rU')
    total_data = RAW.read()
    data_block = re.split( "\n(?:DETAIL REPORT|SUMMARY BY [A-Z]+)\n",total_data    )
    print(len(data_block))
    print("\n\n\n\n\n######################\n\n\n\n".join(data_block) )
    