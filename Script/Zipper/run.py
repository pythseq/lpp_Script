#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/7/19


from lpp import *
from  termcolor import colored
import subprocess,shlex
from optparse import OptionParser
from configure import cele_path
def get_para(   ):
    #获得运行参数
    usage = '''
	%prog [ options ]
	'''
    parser = OptionParser( usage = usage  )


    parser.add_option("-g", "--GKP", action="store",
                      dest="gkp",
                      help="gatekeeper directory")

    parser.add_option("-t", "--Tig", action="store",
                      dest="tig",
                      help="Tigstore directory")

    parser.add_option("-u","--UNI",action= "store",
                      dest = "uni",
                      help="Unitig directory"
                      )
    parser.add_option("-r","--READS",action= "store",
                      dest = "read",
                      help="Reads fasta format!"
                      )
    parser.add_option("-c","--REF",action= "store",
                      dest = "reference",
                      help="Reference sequence fasta format!"
                      )	
    parser.add_option("-e","--TER",action= "store",
                      dest = "terminal",
                      help="Terminal direcotry"
                      )	
    parser.add_option("-o","--OUT",action= "store",
                      dest = "output",
                      help="output file"
                      )			
    parser.add_option("-v","--OVLA",action= "store",
                      dest = "overlap",
                      help="overlap store location!!"
                      )			

    (options, args) = parser.parse_args()
    return options,args
if __name__=='__main__':
    print( colored(  "Step1 Preparing!!",'blue')   )
    options,args = get_para()
    gkp = options.gkp
    tig = options.tig
    uni = options.uni
    overlap = options.overlap
    read  = options.read
    reference = options.reference
    termin = options.terminal
    output = options.output
    cache_path = './cache/'
    if not  os.path.exists(  cache_path  ):
        os.mkdir(  cache_path )
    print ( colored( "Preparing ok!!",'green' )  )
    print( colored(  "Step1 Get best reads!!!!",'blue' )  )
    best_output = cache_path+'best.fasta'
    best_reads_command = cele_path+'''/get_best_reads.py -b %(unig)s -r %(read)s -o %(best)s'''%( 
        {
            'unig':uni,
            'read':read,
            'best':best_output,
        } 
                                                                                                  )

    err = subprocess.Popen(  shlex.split( best_reads_command ),stderr=subprocess.PIPE  ).communicate()
    if not err[0]:
        print( colored("Extracting best reads OK!!","green")  )
    else:
        print(colored(err[0],'red'))
        print( colored('Step1 Error!','red') )
        sys.exit()    

    #开始进行参考图的构建
    print(  colored("Step2 Align best reads to Reference. Running!!" ,'blue')    )
    reference_output = cache_path+'reference_graph'

    reference_commandline = cele_path+'''/celera_blat.py -r %(reference)s -b %(best_reads)s -o%(out)s'''%( 
        {
            'reference':reference,
            'best_reads':best_output,
            'out':reference_output
        }
    )

    err = subprocess.Popen(  shlex.split( reference_commandline ),stderr=subprocess.PIPE  ).communicate()
    if  not err[0]:
        print( colored("best reads alignment OK!!",'green')  )
    else:
        print(err[0])
        print( 'Step2 Error!' )
        sys.exit()	










    #开始运行celera_zipper.py
    print( colored(  "Step3 Zipper start running!!!!",'blue' )  )
    zipper_output = cache_path+'unitig_graph'
   
    zipper_commandline = cele_path+'''/celera_zipper.py  -k %(reference_output)s -g %(gkp)s -t %(tig)s -u %(uni)s -e %(termin)s -o %(out)s -b %(best_reads)s'''%( 
        {'gkp':gkp,
         'tig':tig,
         'uni':uni,
         
         'termin':termin,
         'out':zipper_output,
         'best_reads':best_output,
         'reference_output':reference_output,
         }  
    )
    print( zipper_commandline )
    os.system( zipper_commandline )
    print( colored("Zipper OK!!","green")  )


    #对拼接网络进行校正
    print( colored( "Step5 Network Correction,  Running!!" ,'blue')    )
    correct_output = cache_path+'CorrectNetwork'
    correct_commandline = cele_path+'''/get_reference_network.py -g %(unitig_graph)s  -u %(uni)s -c %(reference)s  -o %(out)s -v %(overlap)s'''%( 
        {'unitig_graph':zipper_output,
         'uni':uni,
         'reference':reference_output,
         'out':correct_output,
         'overlap':overlap
         }  
    )

    err = subprocess.Popen(  shlex.split( correct_commandline ),stderr=subprocess.PIPE  ).communicate()
    if  not err[0]:
        print( colored("Step5 Successful!!",'green')  )
    else:
        print(colored(err[0],'red') )
        print( colored('Step5 Error!','red') )
        sys.exit()	

    #对矫正的结果进行拼接
    print(  colored('Step6 Assembly Contig !!','blue')   )
    assembly_output = output
    assembly_commandline = cele_path+'''/assemly_need.py -i %(correct)s -o %(out)s -u %(uni)s   -r %(unitig_graph)s  '''%( 
        {'unitig_graph':zipper_output,
         'uni':'./unitig.fasta',
         'correct':correct_output,
         'out':assembly_output,
         }  
    )

    err = subprocess.Popen(  shlex.split( assembly_commandline ),stderr=subprocess.PIPE  ).communicate()
    if  not err[0]:
        print( colored("Running Successful!!",'green')  )
    else:
        print(colored(err[0],'red') )
        print( colored('Step6 Error!','red') )
    sys.exit()		