#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2016/3/9
"""
from Dependcy import *
from optparse import OptionParser
from Taxon_GI_Parse import *
import re
nr_data = pd.read_table(sys.argv[1])
GENE_TAXON =  open( "Taxon_Taxon.txt",'w' )
GENE_STATS =  open( "Taxon__TaxonStats.txt",'w' )
taxon_stat_hash = Ddict()
for i in xrange(0,len(nr_data)):
    gi = re.search("gi\|(\d+)",nr_data.loc[i,"Nr_Hit"])
    if gi:
        gi = gi.group(1)
        taxon_gi_sql = Taxon_GI.select(Taxon_GI.q.GI==int(gi) )   
        if taxon_gi_sql.count():
            taxon_gi_sql = taxon_gi_sql[0]
            taxon_id = taxon_gi_sql.Taxon
            taxon_name_sql = TaxonName.select(TaxonName.q.Taxon==taxon_id)   
            try:
                taxon_name = taxon_name_sql[0].Name
    
                GENE_TAXON.write( nr_data.loc[i,"Name"] +'\t'+taxon_name+'\n'  )

                taxon_stat_hash[taxon_name][ nr_data.loc[i,"Name"] ]=""
            except:
                pass
total = 0
for taxon in taxon_stat_hash:
    total+=len(taxon_stat_hash[taxon])
    
for key in sorted( taxon_stat_hash,key= lambda x: len( taxon_stat_hash[x]  )   )[::-1]:

    GENE_STATS.write(   key+'\t%s'%(  len( taxon_stat_hash[key]  )  ) +'\t'+str(  1.0*len( taxon_stat_hash[key]  )/total   )+'\n'  )

    