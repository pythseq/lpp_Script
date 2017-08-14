#!/usr/bin/nextflow
params.query = "$HOME/Scaffold.fa"

 
/*
 * Given the query parameter creates a channel emitting the query fasta file(s),
 * the file is split in chunks containing as many sequences as defined by the parameter 'chunkSize'.
 * Finally assign the result channel to the variable 'fasta'
 */
scaff = file("$params.query")
outputpath = scaff.getParent()

 Channel
    .fromPath(params.query)
    .into { scaffold_rep; scaffold_pro; scaffold_build ;scaffold_den;scaffold_raw }
 
/*
 * Executes a BLAST job for each chunk emitted by the 'fasta' channel
 * and creates as output a channel named 'top_hits' emitting the resulting
 * BLAST matches 
 */
process RepeatMasker {

    input:

		file 'scaff.fa' from scaffold_rep
 
    output:
		file 'masked/*.gff' into repeatmaker_out
 
    """
    mkdir masked; RepeatMasker -e ncbi -pa 8 -norna -dir masked -gff -html HTML scaff.fa
    
    """
}

process RepeatPro {

    input:
		file 'scaff.fa' from scaffold_pro

 
    output:
		file '*.gff3' into repeatmaker_pro
 
    """
    /pub/SOFTWARE/Other/RepeatMasker/RepeatProteinMask      -engine  ncbi scaff.fa
	RepeatProteinMaskResultTrans.py  *.annot Protein.gff3
    
    """
}

process RepeatDenovo_BuildDatabase {

    input:
		file 'scaff.fa' from scaffold_build

 
    output:
		file 'Database*' into database
 
    """
     BuildDatabase -name Database  scaff.fa
    
    """
}

process RepeatDenovo_Modeler{
	input :
		file db from database
	output :
		file "RM_*/consensi.fa.classified" into denovobase
	"""
	 RepeatModeler -database Database
	"""

}
 
process RepeatDenovo_Masker{
	input:
		file db from denovobase
		file 'scaff.fa' from scaffold_den
	output:
		file "Denovo/*.gff" into repeatmaker_deno
		file "Denovo/*.tbl" into repeatmaker_table
	"""
		mkdir Denovo ; RepeatMasker -e ncbi  -pa 8 -lib $db -dir Denovo -gff -html scaff.fa
	
	"""
		}
		
process Integrate{
	publishDir "$outputpath/RepeatMasked/", mode: 'copy', overwrite: true
	input:
		file "Denovo.gff3" from repeatmaker_deno
		file "Protein.gff3" from repeatmaker_pro
		file "Rep.gff3" from repeatmaker_out
		file "Scaffolds.fa" from scaffold_raw
		file "RepeatMasker.tbl" from repeatmaker_table
	output:
		file "Repeat.gff3" into RepeatGFFResult
		file "Scaffolds.Masked.fasta" into RepeatSeqResult
		file "*.tsv" into ResultTable
	
	
	"""
		 cat Denovo.gff3  Protein.gff3  Rep.gff3 > combined.gff
		 bedtools  sort  -i combined.gff  >All.gff
		 bedtools  merge -c 2,3,6,7,8,9  -o distinct -i All.gff  | cut -f 1,4,5,2,3,6,7,8,9 >merged.gff
		 
			 
		RepeatMaskerSequenceFromGFF.py -i Scaffolds.fa  -g merged.gff  -o Scaffolds.Masked.fasta
		cp RepeatMasker.tbl RepeatMasker.tsv
		 awk '{print($1,"\t",$4,"\t",$9,"\t",$2,"\t",$3,"\t",".","\t","+","\t",".","\t","")}' merged.gff  > Repeat.gff3
	"""
}
 


 
 
 
 
 
 
 
 
 
 
 
 
 
