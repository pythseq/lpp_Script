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
    if "0 putative CRISPR arrays found." in total_data:
        END = open(output_path+'Result.txt',)
        END.write("0 putative CRISPR arrays found.")
        sys.exit()
        
    data_block = re.split( "\n(?:DETAIL REPORT|SUMMARY BY [A-Z]+)\n",total_data    )
    align_detail = data_block[1]
    align_detail = align_detail.strip()
    detail_list = re.split("\n{3}",align_detail)
    SPACER_SEQ = open(output_path+'/Spacer.fa','w')
    SPACER_TSV = open(output_path+'/Spacer.xls','w')
    SPACER_TSV.write( '\t'.join( ["Name","Kind","Function","Ref_Source","Ref_Start","Ref_Stop","Ref_Frame"	,"Seq_Nucleotide",	"Seq_Nucl_Length"]+'\n' )
 )
    AlignList = namedtuple("Align","Pos,Repeat,iden,SpacerLength,Left,Repeat,Spacer")
    for each_detail in detail_list:
        crispr_number = re.search("Array\s+(\d+)",each_detail).group(1)
        seq_name = re.search(">(\S+)",each_detail).group(1)
        data_line_list = each_detail.split("\n")
        data_line_list = data_line_list[5:]
        spacerid = 0 
        for key in data_line_list:
            align_list = key.split()
            if key.startswith("=="):
                break
            if len(align_list)!=7:
                continue
            spacerid+=1
            AlignList._make(align_list)
            startpos = int(AlignList.Pos)
            repeat_length = int(AlignList.Repeat)
            spacer_start = startpos+repeat_length
            spacer_end = spacer_start+int(AlignList.SpacerLength)
            spacer_name = seq_name+"_Crispr%sSpacer%s"%(crispr_number,spacerid)
            
            spacer_name = SPACER_TSV.write(
                "\t".join(
                    [
                        spacer_name
                        
                        
                    
                    ]
            
            
                )
            )
            
            
            
            
            
            )
            
    
    