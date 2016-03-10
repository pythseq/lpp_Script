#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/4
"""
from lpp import *
from bs4 import BeautifulSoup
import tempfile
import pandas as pd
from optparse import OptionParser
import poster,time,urllib2,urllib
from poster.encode import multipart_encode  
from poster.streaminghttp import register_openers 
register_openers() 
usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--Sequence", action="store",
                  dest="Sequence",

                  help="Genome Sequence in fasta format")
parser.add_option("-o", "--out", action="store",
                  dest="outputprefix",

                  help="oututprefix")

# parser.add_option("-a", "--Alignment", action="store",
            # dest="Alignment",

            # help="IS alignment")

# parser.add_option("-s", "--nul", action="store",
            # dest="Nul",

            # help="Nul Seq for IS")
# parser.add_option("-t", "--stat", action="store",
            # dest="STAT",

            # help="IS Staistics infomation")


if __name__ == '__main__':
    (options, args) = parser.parse_args()
    DATA = fasta_check( open(options.Sequence,'rU') )
    outputprefix = options.outputprefix
    outputpath = check_path(  os.path.dirname( outputprefix   )   )
    README = open(outputpath+'/Readme','w')
    README.write(   
"""
使用在线网站ISFINDER（https://www-is.biotoul.fr/）预测IS序列，使用blastn+e value 1e-5作为参数
包含以下结果：
*.fa预测到的IS序列
*.xls IS预测结果的表格
*.stat IS预测结果的统计结果，用excel打开！！

    
    
    """)
    
    url = "https://www-is.biotoul.fr/blast/ncbiIS.php"
    values = {
	"title":"",
        "prog":"blastn",
	"blast":"ok",
	"wordsize":11,
	"database":"ISfindernt",
        "seqfile":open(options.Sequence,'rb'),
        "seq":"",
        "expect": "1e-500"	,
	"gapcosts":"5 2"
    }	
    datagen, headers = poster.encode.multipart_encode(values) 


    sequence = re.sub('\s+','',DATA.next()[-1])
    NUL = open( outputprefix+".fa",'w'  )
    STAT = open( outputprefix+".stat",'w'  )

    is_stat = Ddict()
    data = urllib.urlencode(values)
    req = urllib2.Request(url,datagen, headers)
    response = urllib2.urlopen(req)
    try:
        uploadend = response.read()
        print(  uploadend )

        out_url = re.search("""(resultat.php\S+\"\>)""", uploadend).group(1)

        result = None
        while not  result:
            time.sleep(5)
            end_output = urllib.urlopen("https://www-is.biotoul.fr/blast/"+out_url).read()
            if "Query=" in end_output:
                data = end_output.split("</article>")[0]
                data_list  = data.split("<b>Query=")[1:] 
                for e_b in data_list:
                    e_b = e_b.replace("</td>","\t</td>").replace("</th></tr>","\n").replace("</th>","\t</th>")
                    data = BeautifulSoup(e_b,"html5lib")
                    
                    print( data.get_text() )                
                sys.exit()
            result = re.search("Normal view</a></font><br>(.*)</form>",end_output,re.DOTALL)
        result = result.group(1)
        if result:
            ALN = open( outputprefix+".xls",'w'  )
            STAT.write("IS_name\tNumber\tAverage.Length\n")

            ALN.write( '\t'.join(["Name","Ref_Source","Kind","Function","Ref_Start","Ref_Stop","Ref_Frame","Seq_Nucl_Length","Seq_Nucleotide","IS_SeqenceIdentity","IS_AlignmentLength","IS_Mismatch","IS_GapLength","IS_QueryStart","IS_QueryEND","IS_RefStart","IS_RefEnd","IS_Evalue","IS_Bitscore"])+'\n' )
            i=0

            has = {}
            for line in result.split("\n")[:-1]:
                if line in has:
                    continue
                has[line] = ""
            for line in  sorted( has,key = lambda x: int(x.split("\t")[6])   ):
                i+=1
                line_l = line.split("\t")
                chro_name = re.sub("_+$","",line_l[0].split("|")[-1])
                out_data = []
                isname= chro_name+"_IS%s"%(i)

                q_start,q_end = int(line_l[6]),int(line_l[7])
                if q_start <q_end:
                    frame='+'
                else:
                    frame='-'
                    q_start,q_end  = q_end,q_start
                is_seq = sequence[q_start:q_end]
                NUL.write('>'+isname+' '+line_l[1]+'\n'+is_seq+'\n')
                is_stat[ line_l[1] ][ isname ]=is_seq

                is_length = len(is_seq)
                out_data.extend([isname,chro_name,"IS_Element",line_l[1],line_l[6],line_l[7],frame,str(is_length),is_seq])
                out_data.extend(line_l[2:])
                ALN.write("\t".join(out_data)+'\n')
        else:
            STAT.write(  "Not Find IS!!"  )			
    except Exception,error:
        print(error)
    for key in is_stat:
        STAT.write(   key+'\t%s'%( len(is_stat[key]  )   )   )
        all_length = 0
        for key2,seq2 in is_stat[ key ].items():
            all_length+= len(seq2)

        ave_length = all_length/len(is_stat[key] )
        STAT.write( '\t%s\n'%(  ave_length  ) )

