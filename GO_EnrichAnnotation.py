#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
from lpp import *
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-o", "--Output", action="store",
                  dest="OutputPrefix",

                  help="OutputPrefix")

parser.add_option("-g", "--GO", action="store",
                  dest="ALLGO",
                  help="AllGO Mapping File")

parser.add_option("-d", "--Diff", action="store",
                  dest="Diff",

                  help="Gene Different File")
parser.add_option("-a", "--Annotation", action="store",
                  dest="Anno",

                  help="Gene Annotation File")


parser.add_option("-e", "--Enrich", action="store",
                  dest="Enrich",

                  help="Gene Enrichment File")



if __name__ == '__main__':
	(options, args) = parser.parse_args()
	
	#Extract All Differental Gene Annotation
	all_diff_gene = pd.read_table(options.Diff)
	all_Annotaion = pd.read_table( options.Anno )
	all_diff_anno = all_Annotaion[ all_Annotaion["Name"].isin( all_diff_gene["id"]  )  ]
	
	all_go = pd.read_table( options.ALLGO )
	all_enrichgo = pd.read_table( options.Enrich )
	all_enrichgo_gene = all_go[ all_go["GOTerm"].isin( all_enrichgo["category"]  )  ]
	
	
	enrich_go_annotation = pd.merge(
	    left=all_enrichgo_gene, 
	    right = all_diff_anno,
	    left_on = "Gene",
	    right_on = "Name",
	    how="inner"
	    
	)
	del  enrich_go_annotation["Name"]
	enrich_go_annotation.to_csv(options.OutputPrefix+'.Annotation.tsv',sep = "\t",index = False)
	
	