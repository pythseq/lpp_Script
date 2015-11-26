#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/25
"""

from lpp import *
import pandas
from optparse import OptionParser
def Pagan( input_file  ):
    global Ortholog_Pair
    input_file = os.path.abspath( input_file  )
    path = os.path.split(input_file)[0]+'/'
    output = path+'outfile'
    ancestor = path+'ancestor'
    os.system("pagan --seq %s --threads 64 --silent -o %s   "  %(  input_file, output ))
    RAW = fasta_check( open( output+".fas" ,'rU'   ) )
    t,s = RAW.next()
    s = re.sub("\s+", "" , s)
    if s.count("-")/len(s)>0.4:
        Ortholog_Pair[orthId][ "AncestorySeq" ] = "-"
        return "Too Divergent!!"
    os.system("pagan --ref-seqfile %s.fas  --ref-treefile %s.tre  --output-ancestors -o %s  --threads 64 --silent"%( output,output,ancestor  ))
    for t,s in fasta_check(  open( "%s.fas"%(ancestor),'rU'   )  ):
        if "#1#" in t:

            return s
        
def CdsFinder( input_file   ):
    path = os.path.split(input_file)[0]+'/'
    data_hash = Ddict()
    os.system(" TransDecoder -t %s"%(input_file))
    CDS = fasta_check(open( "%s.transdecoder.cds"%(input_file),'rU'  ))
    for t,s in CDS:
        name = t[1:].split("|")[0]
        [(start,end,frame)] = re.findall( "\:(\d+)\-(\d+)\((\S)\)",t  )
        if name not in data_hash:
            data_hash[ name ]["Seq"] = s
            data_hash[ name ]["start"]=start
            data_hash[ name ]["end"]=end
            data_hash[ name ]["frame"]=frame
        elif len(s) >len(data_hash[ name ]["Seq"]):
            data_hash[ name ]["Seq"] = s
            data_hash[ name ]["start"]=start
            data_hash[ name ]["end"]=end
            data_hash[ name ]["frame"]=frame                
    if len(data_hash)==3:
        END = open(path+"all_cds.fa",'w')
        LOC = open(path+"Location.tsv",'w')
        for key in data_hash:
            if "Ancestor" not in key:
                ALL_SEQ.write('>'+key+'|CDS'+'\n'+data_hash[key][ "Seq" ])
                Ortholog_Pair[orthId]["AncestorCDS"] = data_hash[key][ "Seq" ][:-1]
                Ortholog_Pair[orthId]["AncestorCDS_start"] = data_hash[key][ "start" ]
                Ortholog_Pair[orthId]["AncestorCDS_end"] = data_hash[key][ "end" ]
                Ortholog_Pair[orthId]["AncestorCDS_frame"] = data_hash[key][ "frame" ]
            elif "mian" not in key:
                Ortholog_Pair[orthId]["mianCDS"] = data_hash[key][ "Seq" ][:-1]
                Ortholog_Pair[orthId]["mianCDS_start"] = data_hash[key][ "start" ]
                Ortholog_Pair[orthId]["mianCDS_end"] = data_hash[key][ "end" ]
                Ortholog_Pair[orthId]["mianCDS_frame"] = data_hash[key][ "frame" ]     
            else:
                Ortholog_Pair[orthId]["yanCDS"] = data_hash[key][ "Seq" ][:-1]
                Ortholog_Pair[orthId]["yanCDS_start"] = data_hash[key][ "start" ]
                Ortholog_Pair[orthId]["yanCDS_end"] = data_hash[key][ "end" ]
                Ortholog_Pair[orthId]["yanCDS_frame"] = data_hash[key][ "frame" ]                     
            END.write('>'+key+'\n'+data_hash[key][ "Seq" ])
            
            LOC.write( key+'\t'+data_hash[key][ "start"  ]+'\t'+ data_hash[key][ "end"  ]+'\t'+ data_hash[key][ "frame"  ]+'\n')
        return END.name
    else:
        return "Not Enough CDS"
    
def KaksCal(  input_file  ):
    global Ortholog_Pair
    output = input_file.replace(".cds",".cds.maff",'w')
    path = os.split(input_file)[0]+'/'
    os.system("pagan --seq %s --threads 64 --silent -o %s   "  %(  input_file, output ))
    output_trimed = output+"_trimed"
    os.system("""trimal -in  %s  -fasta |sed -r "s/\s+[0-9]+\s+bp//g" >%s """%( output ,output_trimed ) )
    cache_hash = {}
    for t,s in fasta_check( open( output_trimed,'rU'  )  ):
        if "mian" in t:
            cache_hash["mian"] = s
        elif "yan" in t:
            cache_hash["yan"] = s
        else:
            cache_hash["Ances"] = s
    mian_ances_name = path+"mian_vs_ances.axt"
    M_A = open( mian_ances_name,'w' )
    M_A.write("Mian_vs_Ancestor\n")
    M_A.write(  cache_hash["Ances"]+'\n'+cache_hash["mian"]+'\n'   )
    mian_kaks = path+"/Mian_Anc.kaks"
    os.system(  "KaKs_Calculator  -i %s -o %s "%(M_A.name, mian_kaks)  )
    RAW = open( mian_kaks,'rU'  )
    RAW.next()
    Ortholog_Pair[orthId]["KA/KS Harm"] = RAW.next().split("\t")[4]
    
    yan_ances_name = path+"yan_vs_ances.axt"
    Y_A = open( yan_ances_name,'w' )
    Y_A.write("Yan_vs_Ancestor\n")
    Y_A.write(  cache_hash["Ances"]+'\n'+cache_hash["yan"]+'\n'   )
    yan_kaks = path+"/Yan_Anc.kaks"
    os.system(  "KaKs_Calculator  -i %s -o %s "%(M_A.name, yan_kaks)  ) 
    RAW = open( yan_kaks,'rU'  )
    
    RAW.next()
    Ortholog_Pair[orthId]["KA/KS Has"] = RAW.next().split("\t")[4]        

    



if __name__=="__main__":
    '# you could type [  SCRIPT_NAME  ] -h to see the help log !!!!'
    usage='''usage: python %prog [options]

    Calcite KAKS '''
    parser = OptionParser(usage =usage )

    parser.add_option("-i", "--Table", action="store",
                      dest="Table",
                      type='string',
                      help="Ortholog Table")		




    parser.add_option("-o", "--Output", action="store", 
                      dest="output_Path",
                      help="Output Path prefix")
    (options, args) = parser.parse_args()
    outPATH = os.path.abspath(options.output_Path)+'/'
    if not os.path.exists(outPATH):
        os.makedirs(outPATH)
    OrthoTable = pandas.read_table(options.Table)
    table_need = OrthoTable.loc[:,["Ortholog","H.armID","H.armSeq","H.asID","H.asSeq"]]
    Ortholog_Pair = Ddict()
    ALL_SEQ = open(outPATH+"Total_cds.fasta",'w')
    for i in xrange(0,len(OrthoTable)):
        table_data = OrthoTable.loc[i]
        
        orthId = table_data["OrthologID"]
        path_name = outPATH+orthId+'/'
        Ortholog_Pair[orthId][ "HarmId" ] = table_data[ "H.armID" ]
        Ortholog_Pair[orthId][ "HasId" ] = table_data[ "H.asID" ]
         
        if not os.path.exists(path_name):
            os.makedirs( path_name )
            
        RAW_SEQ = open(path_name+"/Unigene.fa",'w')
        RAW_SEQ.write(">"+table_data[ "H.armID" ]+'\n'+table_data[ "H.armSeq" ]+'\n'+ ">"+table_data[ "H.asID" ]+'\n'+table_data[ "H.asSeq" ]+'\n' )
        RAW_SEQ.close()
        ancestor = Pagan(RAW_SEQ.name)
        Ortholog_Pair[orthId][ "AncestorSeq" ] = ancestor[:-1]
        
            
            
        
        if "Too " in ancestor:
            Ortholog_Pair[orthId][ "KA/KS Harm" ] = ancestor
            Ortholog_Pair[orthId][ "KA/KS Has" ] = ancestor     
        else:
            CDSPREDECTION  = open(path_name+"CDS_Predection.fa",'w'  )
            CDSPREDECTION.write( ">"+table_data[ "H.armID" ]+'\n'+table_data[ "H.armSeq" ]+'\n'+ ">"+table_data[ "H.asID" ]+'\n'+table_data[ "H.asSeq" ]+'\n'+">Ancestor_%s\n"%(orthId)+ancestor+'\n'   )
            CDSPREDECTION.close()
            cds_name = CdsFinder(CDSPREDECTION.name)
            if "Not " in cds_name:
                Ortholog_Pair[orthId][ "KA/KS Harm" ] = cds_name
                Ortholog_Pair[orthId][ "KA/KS Has" ] = cds_name
                
            else:
                KaksCal(cds_name)
                
    ALL_SEQ.close()
    KAKS_Result = open( outPATH+"/KAKS_Result.tsv",'w'   )
    KAKS_Result.write("OrthologID"+'\t')
    KAKS_Result.write(    '\t'.join(  sorted( Ortholog_Pair[ orthId ] )    ) +'\n'    )
    for orthId in Ortholog_Pair:
        KAKS_Result.write(orthId)
        for key in sorted( Ortholog_Pair[ orthId ]  ):
            KAKS_Result.write('\t'+Ortholog_Pair[ orthId ][ key ] )
        
        KAKS_Result.write('\n')