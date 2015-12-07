#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/6
"""
from Dependcy import *
from optparse import OptionParser

if __name__=="__main__":
    config_hash = Config_Parse()
    usage = '''usage: python2.7 %prog'''
    parser = OptionParser(usage =usage ) 
    parser.add_option("-p", "--PEP", action="store", 
                      dest="PEP", 
                      default = "",
                      help="protein file")
    parser.add_option("-n", "--NUL", action="store", 
                      dest="NUL", 
                      help="necleotide file")		

    parser.add_option("-o", "--end", action="store", 
                      dest="output_prefix", 
                      help="output_prefix")

    parser.add_option("-e", "--evalue", action="store", 
                      dest="evalue", 
                      help="evalue cutoff")



    (options, args) = parser.parse_args() 
    FASTA = fasta_check(open(options.PEP,'rU'))
    sequence = FASTA.next()[-1]
    blast_type = Nul_or_Protein(sequence)
    output_prefix = os.path.abspath(  options.output_prefix )
    out_put_path = os.path.split(output_prefix)[0]+'/'
    tag = "%s"%( os.getpid() )
    if not os.path.exists( out_put_path ):
        os.makedirs( out_put_path )

    diamond_result = output_prefix+'.tsv'
    proteinseq = options.PEP
    if not proteinseq:
        proteinseq = options.NUL
        
    error = RunDiamond(proteinseq,options.evalue, blast_type,"kegg",diamond_result)
    if error:
        print( colored("%s 's KEGG process in Diamond of kegg is error!!","red") )
        print(colored( error,"blue"  ))
        print(  "##############################################"   )

        sys.exit()

    blast_mapping_command = config_hash["Utils"]["gapmap"]+'/blast_sql.py -f %(diamond)s   -r  %(diamond)s   -1 forward -2 forward  -n Forward -N Reverse -p %(pep)s -d %(dna)s -x %(tag)s -q'%(
        {
            "diamond":diamond_result,
            "pep":proteinseq,
            "dna":options.NUL,

            "tag":tag
        }
    )
    blast_mapping_process = subprocess.Popen( blast_mapping_command.split(),stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
    blast_mapping_process.communicate()




    source_location = out_put_path+'/source/'
    source_command = config_hash["Utils"]["gapmap"]+"/Mapping_sql.py -o %s -d %s"%(
        source_location,
        tag,
        ) +" && "+config_hash["Utils"]["gapmap"]+"/Show_all_Mapping.py -o %s  -d %s"%(
            output_prefix,
            tag,
        )
    source_process = subprocess.Popen( source_command.split(),stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
    source_process.communicate()
    pathway_detail_frame = pd.read_table( "%s_detail.tsv"%(  output_prefix  )   )
    # os.remove( "%s_detail.tsv"%(  output_prefix  ) )
    
    pathway_stats_command = config_hash["Utils"]["gapmap"]+"/Pathway_stats.py %(name)s %(out)s_PathwayCategoery.tsv %(out)_PathwayCategory_Stats.stat"%(
                {
                    "name":tag,
                    "out":output_prefix
                }
                )
    pathway_stats_process = subprocess.Popen( pathway_stats_command.split(),stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
    pathway_stats_process.communicate()
    pathway_category_frame = pd.read_table("%s_PathwayCategoery.tsv"%(output_prefix) )
    
    pathway_result_frame = pd.merge( pathway_detail_frame,pathway_category_frame,left_on='Name', right_on='Name', how='outer' )
    pathway_result_frame.to_csv( "%s_pathway_detail.xls"%(output_prefix),sep="\t",index=False  )
    # os.remove("%(out)s_PathwayCategoery.tsv"%(
    # {
        # "out":output_prefix
    # }
    # )  
              # )


    pathwaydraw_command = "Pathway_Draw.py   -i %s_pathway_detail.xls  -o %s -r %s"%(
        output_prefix,
        out_put_path+"stats",
        out_put_path+'Draw.R',
    )
    pathwaydraw_process = subprocess.Popen(  pathwaydraw_command.split(),stderr= subprocess.PIPE,stdout=  subprocess.PIPE  )
    stdout,stderr = cogdraw_process.communicate()	






