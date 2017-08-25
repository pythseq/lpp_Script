#!/usr/bin/nextflow
params.query = "./"
/*
 * Given the query parameter creates a channel emitting the query fasta file(s),
 * the file is split in chunks containing as many sequences as defined by the parameter 'chunkSize'.
 * Finally assign the result channel to the variable 'fasta'
 */
outputpath = "./"

Channel
    .fromPath(params.query)
    .into { Prokka_input }
 
/*
 * Executes a BLAST job for each chunk emitted by the 'fasta' channel
 * and creates as output a channel named 'top_hits' emitting the resulting
 * BLAST matches 
 */

 process PROKKA {
	maxForks 6
	publishDir "$outputpath/Annotation/", mode: 'copy', overwrite: true

    input:

		file Scaff from Prokka_input
 
    output:
		file '*.tar.gz' into Annotation
 
    """
	 Contig_Combine.py  $Scaff  Scaff.fa
	 /pub/SOFTWARE/Other/prokka-1.11/bin/prokka   Scaff.fa  --force  --prefix ${Scaff.getBaseName()} --outdir ${Scaff.getBaseName()} --evalue 1e-5  --genus test --strain ${Scaff.getBaseName()}  --cpus 64 --compliant --quiet  --locustag ${Scaff.getBaseName()}
	 tar -zcf ${Scaff.getBaseName()}.tar.gz ${Scaff.getBaseName()}/
	 
    """
}

 
 
 
