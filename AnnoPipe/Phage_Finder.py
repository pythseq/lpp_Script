#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/15
"""
from lpp import *
from optparse import OptionParser
usage = '''usage: python2.7 %prog [options] 
         parse eggNOG data

        '''
parser = OptionParser(usage =usage )    
parser.add_option("-i", "--Input", action="store",
                dest="name",
                help="Input sequence name")
parser.add_option("-o", "--out", action="store",
                dest="outprefix",
                help="output path")


if __name__ == '__main__':
	(options, args) = parser.parse_args()
	seqname = options.name
	prefix = os.path.basename(seqname)
	outpath = options.outprefix+'/'+prefix+'/'
	outpath = check_path(outpath)
	outputname = outpath+prefix+'_Phage'
	os.system( " phage_finder_v2.0.sh  %s  %s"%(seqname,outpath)  )
	for e_f in glob.glob(outpath+"*.*"):
		if e_f.endswith(".hmm3") or e_f.endswith(".out") or e_f.endswith(".log"):
			os.remove(e_f)
		else:
			path,file_name = os.path.split(e_f)
			appendix = file_name.rsplit(".",1)[-1]
			shutil.move(e_f,outputname+'.'+appendix)
			
	if os.path.getsize(outputname+'.pep'):
		XLS = open(outputname+"_PhageGene.xls",'w')
		XLS.write("Name\tBelongToPhage\n")
		for t,s in fasta_check(  open(outputname+'.seq'   )   ):
			name,phage = t[1:].strip().rsplit("_",1)
			XLS.write(name+'\t'+prefix+'_'+phage+'\n')
		con_data = Ddict()
		PHAGEXLS = open(outputname+"_PhageElement.xls",'w')
		PHAGEXLS.write("Name\tKind\tFunction\tRef_Source\tRef_Start\tRef_Stop\tRef_Frame\tSeq_Nucleotide\tSeq_Nucl_Length\n")
		for t,s in fasta_check( open(outputname+'.con','rU')):
			s = re.sub("\s+", "", s)
			[(start,end)] = re.findall( "\((\d+)\-(\d+) bp\)",t)
			length = int(end)-int(start)+1
			phage_name = t.split()[0].rsplit("_",1)[-1]
			phage_function = re.search("\S+\s+(.+)\s+\(",t).group(1)
			PHAGEXLS.write( prefix+'_'+phage_name+"\tPhageElement"+'\t'+phage_function+'\t'+prefix+'\t'+start+'\t'+end+'\t+\t'+s+'\t'+str(length)+'\n'  )
			
			
			
	