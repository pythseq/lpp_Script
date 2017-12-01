#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/1/8

from Bio import SeqIO
from lpp import *
from Bio.SeqRecord import SeqRecord
import itertools

RECORD = SeqIO.parse( sys.argv[1],'genbank' )
GENE = open( sys.argv[2]+'.fnn','w' )
PRO = open( sys.argv[2]+'.fna','w' )
ANNO = open(sys.argv[2]+'.function','w')
from Bio import Seq
SeqRecord.format
for each_data in RECORD:
    
    seq = each_data.seq
    
    #seq = re.sub( '(\w{70})','\\1\n',seq  )
    for each_feature in each_data.features:
        if each_feature.type == 'CDS':
            nul_seq = each_feature.extract( seq ) 
            
            name    = re.sub('\s+','',str(each_feature.qualifiers['locus_tag'][0]))
             
            product = str( each_feature.qualifiers['product'][0] )
	    if "translation" not in each_feature.qualifiers:
		continue
            protein = re.sub('\s+','',each_feature.qualifiers['translation'][0]) 
            nul = re.sub( '(\w{60})','\\1\n', str(each_feature.extract( seq )) )
            
            GENE.write( '>%s\n%s\n'%( name, nul )  )
            PRO.write(   '>%s\n%s\n'%( name, protein  )   )
	    ANNO.write("%s\t%s\n"%(name,product  )  )



