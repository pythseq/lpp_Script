#!/usr/bin/env python
#coding:utf-8
# Author:  LPP --<lpp1985@hotmail.com>
# Purpose: 
# Created: 2011/5/27
from lpp import *


RAW = open( sys.argv[1],'rU'  )

RAW.next()
ko_gene = Ddict()
go_def = File_dict(open('/home/lpp/Database/GO/NAME_DEF.list','rU')).read(1,2)
for line in RAW:

    line_l = line.split('\t')

    name = line_l[0].split()[0]
    ko_all = re.findall("(K\d{5})\:",line_l[1])
    for each_ko in ko_all:
        ko_gene[each_ko][name] = ""

id_go = Ddict()
change_go = File_Ddict( open(  '/home/lpp/Database/GO/relationship.alter','rU'  )  ).read(1,2)
ALL_GO = open( '/pub/Database/Newest_KEGG/ftp.bioinformatics.jp/kegg/genes/ko/ko_go.list','rU'  )
for line in ALL_GO:
    line_l = line.strip().split('\t')
    ko = line_l[0].split(":")[1]
    go = line_l[1].upper()
    if go not in go_def:
        continue
    if ko in ko_gene:
        if go in change_go:
            for each_gene in ko_gene[ko]:
                for alter_go in change_go[go]:
                    id_go[each_gene][alter_go]=''
                    
        else:
            for each_gene in ko_gene[ko]:
                id_go[each_gene][go]=''
END = open("GOAnnotation.tsv",'w')
for e_g in id_go:
    for go in id_go[e_g]:
        END.write(e_g+'\t'+go+'\n')
        

