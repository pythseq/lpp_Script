#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/11/21
"""
import sys,shlex,os,subprocess
from ConfigParser import ConfigParser
import redis
import tempfile
from  termcolor import colored
from lpp import *
from optparse import OptionParser
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--Input", action="store",
                  dest="Input",

                  help="Input Fasta Sequence")
parser.add_option("-o", "--Output", action="store",
                  dest="output",

                  help="Output File")

parser.add_option("-d", "--Database", action="store",
                  dest="Database",

                  help="Database Location")
parser.add_option("-e", "--Evalue", action="store",
                  dest="Evalue",

                  help="Evalue !")
parser.add_option("-n", "--DBName", action="store",
                  dest="dbname",

                  help="DB Name")
parser.add_option("-t", "--Type", action="store",
                  dest="type",

                  help="AlignType, blastx or blastp ,default is blastp",
                  default ="blastp"
                  )

if __name__=="__main__":
    (options, args) = parser.parse_args()
    general_config = ConfigParser()
    redisconfigpath = os.path.split(os.path.abspath(__file__))[0]+'/'
    general_config.read(
        os.path.join( redisconfigpath+"database_redis.ini")
    )
    dbname = options.dbname.lower()
    db_has = general_config.has_option("Redis", dbname)
    if db_has:
        db_number = general_config.get("Redis", dbname)   
        r = redis.Redis(host='localhost',port=6379,db=int(db_number))
    Input = options.Input
    OUTPUT = options.output
    Database = options.Database
    Path = os.path.split(OUTPUT)[0]
    Type = options.type
    if Type not in ["blastx","blastp"]:
        print(colored(  "Type is error! must be blastx or blastp!!!","red"))
        sys.exit()
    if not Path:
        Path="./"
    if not os.path.exists(Path):
        os.makedirs(Path)
    Path = Path+'/'
    E_value = options.Evalue
    query_length = {}
    RAW = fasta_check(open(Input,'rU'))
    for t,s in RAW:
        name = t.split()[0][1:]
        length = str(len(re.sub("\s+", "", s)))
        query_length[name]=length
    temp_name = str(os.getpid())
    tmp_file_name = Path+temp_name
    commandline = """     diamond %s -q %s -d %s  -e %s  --max-target-seqs 1  -p 64 -a %s"""%( 
        Type,
        Input,

        Database,
        E_value,
        tmp_file_name 
    )
    os.system(commandline)
    temp_align_result = tmp_file_name
    END = open(options.output,'w')
    commandline = """ diamond  view  -a  %s  """%(temp_align_result)
    align_result = os.popen(commandline)    
    if not db_has:
        
        
        align_title_list = ["Name","Hit","Identity","AlignmentLength","Mismatch","Gap","QueryStart","QueryEnd","SubjStart","SubjEnd","Evalue","Bitscore"]
        for i in xrange(1,len(align_title_list)):
            align_title_list[i] = dbname+'_'+align_title_list[i]
        END.write( "\t".join( align_title_list ) +'\n' )
        for line in align_result:
            line_l = line.strip().split() 
            END.write('\t'.join(line_l)+'\n')
    else:
        
        align_title_list = ["Name","Hit","Identity","AlignmentLength","Mismatch","Gap","QueryLength","QueryCoverage","QueryStart","QueryEnd","SubjLength","SubjCoverage","SubjStart","SubjEnd","Evalue","Bitscore"]
        for i in xrange(1,len(align_title_list)):
            align_title_list[i] = dbname+'_'+align_title_list[i]
        END.write( "\t".join( align_title_list ) +'\n' )        
        for line in align_result:
            
            line_l = line.strip().split()            
            subj = line_l[1]

            subj_r = r.hgetall(subj)
            subj_length = ""
            subj_coverage = ""
            aln_length  = float( line_l[3] )
            subjaln_length = int(line_l[9]) - int(line_l[8] )+1
            if subj_r:
                
                subj = subj_r["Annotation"]
                subj_length = subj_r["Length"]
                subj_coverage = "%.0f/%s %.2f"%( subjaln_length ,subj_length ,100*subjaln_length/float(subj_length) )
                
            line_l[1] = subj
            end_list = line_l[:6]
            q_length = query_length[line_l[0]]
            end_list.append( q_length    )
            q_alignlength = int( line_l[7]) - int( line_l[6]  )+1
            q_coverage = 100*q_alignlength/float(q_length)
            end_list.append( "(%.0f/%s) %.2f"%( q_alignlength,q_length,  q_coverage   ) )
            end_list.extend(  line_l[6:8] )
            
            end_list.append(  subj_length )
            
            end_list.append( subj_coverage )
            end_list.extend( line_l[8:]  )
            END.write('\t'.join(end_list)+'\n')
            
            

    os.remove(temp_align_result+".daa")