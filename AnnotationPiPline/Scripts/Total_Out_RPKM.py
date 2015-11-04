#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""

#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


db_file = os.path.abspath(sys.argv[1])
Ddatabase_engine = create_engine(  'sqlite:///%s'%(db_file) )
Ddatabase_engine.connect()
Base.metadata.create_all( Ddatabase_engine  )
Session = sessionmaker( bind = Ddatabase_engine  )
session = Session()
END = open(sys.argv[2],'w')
END.write(
    "\t".join(
        [

            "Name",
            "Sequence",
            "Length",
            "Function",
            "RPKM",
            "Nr_Hit",
            "Nr_Eval",
            "Nr_Bitscore",
            "Nr_Identity",
            "Nt_Hit",
            "Nt_Eval",
            "Nt_BitScore",
            "Nt_Identity",            
            "KEGG_Hit",
            "KEGG_Eval",
            "KEGG_BitScore",
            "KEGG_Identity",
            "KEGG_KO",
            "KEGG_PATHWAY",
            "Swiss_Hit",
            "Swiss_Eval",
            "Swiss_BitScore",
            "Swiss_Identity",
            "Eggnog_Hit",
            "Eggnog_Eval",
            "COG",
            "BiologicalProcess",
            "MolecularFunction",
            "CellularComponent"       
        ]
    )+"\n"
)

for i in session.query(AnnotationTable_RPKM).all():
	if not i.Function:
		i.Function="Hypothetical Protein"
	data = [
	    i.Name,
	    i.Sequence,
	    i.Length,
	    i.Function,
	    i.RPKM,
	    i.Nr_Hit,
	    i.Nr_Eval,
	    i.Nr_BitScore,
	    i.Nr_Identity,
	    i.Nt_Hit,
	    i.Nt_Eval,
	    i.Nt_BitScore,
	    i.Nt_Identity,
	    i.KEGG_Hit,
	    i.KEGG_Eval,
	    i.KEGG_BitScore,
	    i.KEGG_Identity,
	    i.KEGG_KO,
	    i.KEGG_PATHWAY,
	    i.Swiss_Hit,
	    i.Swiss_Eval,
	    i.Swiss_BitScore,
	    i.Swiss_Identity,
	    i.Eggnog_Hit,
	    i.Eggnog_Eval,
	    i.COG ,
	    i.BiologicalProcess,
	    i.MolecularFunction,
	    i.CellularComponent,    
	]	
	out_data = []
	for e_data in data:
		if e_data:
			out_data.append(e_data)
		else:
			out_data.append("-")
	END.write(
	   "\t".join(
	      out_data
	      )
	+'\n'
	)
session.commit()
