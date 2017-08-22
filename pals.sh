PALS_Align.py $1 pals_hit.gff3
	piler-64 -trs pals_hit.gff3 -out trs.gff
	mkdir Repeat 
	piler-64  -trs2fasta trs.gff -seq $1  -path Repeat
	mkdir Mafft

	for i in Repeat/*.* ; do echo   "mafft  $i > `Mafft/basename $i.mafft`" >>mafft.sh; done
	cat mafft.sh| parallel -j 64
	mkdir Cons
	for i in Mafft/*.mafft; do piler-64 -cons $i -out Cons/`basename ${i%.*}.cons` -label `basename ${i%.*}`;done
    cat Cons/*.* >Total_Piler.fa
