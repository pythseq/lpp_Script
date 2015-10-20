#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/6/13
from lpp import *
from optparse import OptionParser
import shlex
import subprocess
from configure import celera_assembler
PATH = celera_assembler
def get_nucmer_best( outLine  ):
    '''解析show-coords 的结果 选取最好的结果，并进行排序'''
    outLine = outLine[:-1].split('\n\n')[1]
    outList = outLine.split('\n')[1:]

    all_data = {}
    best = 0
    #将所有的结果进行遍历，寻找最优的结果放在all_data这个hash下，记录起始坐标，比对结果，和方向
    for line in outList:
        line_l = line.split('\t')
        coverage = float( line_l[-3] )
        name = line_l[-1]
        if name not in all_data:
            best = 0
        if coverage >best:
            best = coverage
            start,end = int(  line_l[2]  ), int( line_l[3] )
            location = line_l[:2]
            if start <end:
                tag = '+'

            else:
                tag = '-'


            all_data[ line_l[-1] ]= [ line_l[0] , location , tag  ] 
    """对结果按照坐标进行排序，输出  [  reads[+/-], 起始坐标  ]"""
    output = []
    for key1 in sorted(  all_data, key=lambda x: int( all_data[x][0]  )  ):
        output.append( 
            [ 
                key1+ all_data[ key1 ][-1],    
                [ int(i)   for i in   all_data[ key1 ][1]  ]       
            ]  
        )
    return output





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
    parser.add_option("-e","--TER",action= "store",
                      dest = "terminal",
                      help="Terminal direcotry"
                      )		
    parser.add_option("-o","--OUT",action= "store",
                      dest = "output",
                      help="output file")

    parser.add_option("-b","--BEST",action= "store",
                      dest = "best",
                      help="All needed best reads output"   
                      )		
    (options, args) = parser.parse_args()
    return options,args
def get_value( data ):
    '''建立正向和反向的网络'''
    global overlap_3_network,overlap_5_network
    for i in xrange(0,len(data)-1):
        if data[i][0] =='0' or data[i+1][0] =='0':
            continue
        overlap_3_network[ data[i] ][ data[i+1] ] = ''

    for i in xrange( 1,len( data )  ):
        if data[i][0] =='0' or data[i-1][0] =='0':
            continue		
        overlap_5_network[ data[i] ] [ data[i-1]  ] = ''


libary=string.maketrans('+-','-+')
if __name__=='__main__':


    #得到运行参数
    options,args = get_para()
    gkp = options.gkp
    tig = options.tig
    uni = options.uni
    OUTPUT = open( options.output,'w'  )
    OUTPUT_RAW = open( options.output+'.raw','w'  )
    READ = fasta_check( open( options.read,'rU') )
    best = options.best
    terminal = options.terminal
    ####################

    #获取所有的unitig并存到哈希，unitig的格式为[ 总长，序列  ]
    all_unitig_data= {}
    #获取所有的reads，并打入到hash
    all_reads = {}
    reads_mapping = File_dict(open( glob.glob(tig+'/../*.fastqUIDmap')[0],'rU')).read(3,2)
    for t,s in READ:
        name = t[1:].strip()
        if name in reads_mapping:
            all_reads[reads_mapping[ name ] ] = s


    ##########################################

    #args是运行tigStore获得unitig列表
    #使用子进程调取tigStore而后进行解析
    #all_unitig 
    unitig_args = shlex.split( PATH+'tigStore -g %s -t %s 1 -D unitiglist' % ( gkp, tig) )
    unitig_out = subprocess.check_output( unitig_args  )
    all_unitig = {}
    for i in unitig_out.split('\n')[1:]:
        if not i:
            continue
        all_unitig[ i.split('\t')[0] ] = ''

    ##############################################


    #获取best.edges的最好的图，以二维哈希表示
    #overlap_3_network表示所有的3'关系
    #overlap_5_network表示所有的5'关系
    #每个节点和边都被正向和反向互补后各mapping一次，获得所有的关系

    overlap_3_network = Ddict()
    overlap_5_network = Ddict()

    all_nodes = {}
    for line in open( uni+'/'+'best.edges','rU'):
        if '#' in line:
            continue
        data = []
        line_l = line[:-1].split('\t')
        all_nodes[ line_l[0]  ] = ''
        all_nodes[ line_l[2] ] = ''
        all_nodes[ line_l[4]  ] = ''
        if line_l[3] =="5'":
            tag = '-'
        else:
            tag = '+'

        data.append(  line_l[2]+tag  )
        data.append( line_l[0]+'+'  )
        if line_l[5] =="5'":
            tag = '+'
        else:
            tag = '-'
        data.append( line_l[-2]+tag )

        get_value( data  )

        new_data = [ i.translate( libary )  for i in data[::-1]    ]

        get_value( new_data )

    ######################################################################
    #all_junction包含所有的开叉位点
    ######################################################################

    #进行所有的unitig的解析，将所有unitig内部的reads进行排序，并构建图，与之前的图进行对应
    # all_reads_info 是记录所有的reads的拼接信息，为reads名+方向为键
    #[contig，起始坐标，终止坐标  ]为值，如果一个reads不在best.edges中，则自动跳过
    #unitig_graph记录拼接过程中产生的图，与之前的图进行印证。
    all_reads_info = Ddict()
    unitig_graph_3 = Ddict()
    unitig_graph_5 = Ddict()
    every_contig_detail = Ddict()
    head_unitig = {}
    tail_unitig = {}
    #all_best_reads_need 将涉及拼接并且不随机的所有的best reads 进行提取
    all_best_reads_need = {}
    for each_unitig in sorted(all_unitig ,key = lambda x: int(x)):

        detail_args = shlex.split( PATH+'tigStore -g %s -t %s 1 -d fr -u %s '%( gkp,tig,each_unitig  )  )
        detail_out = subprocess.check_output(  detail_args    )
        cache = []
        i=0
        for line in detail_out.split('\n'):
            if not line:
                continue
            i+=1
            [ ( reads_name,start_loca,end_loca  ) ]= re.findall( 'FRG\s+(\d+)\s+(\d+),\s*(\d+)' ,line )

            if int( start_loca ) <int( end_loca ):
                tag = '+'
            else:
                tag ='-'

            if reads_name not in all_nodes:
                continue

            all_reads_info[  reads_name +tag   ] = each_unitig
            cache.append( reads_name +tag )	

        if cache:
            OUTPUT_RAW.write( each_unitig+'\t'+cache[0]+'\t'+cache[-1]+'\n'   )
        if len( cache)<1:
            for key in cache:				
                for tag in ['+','-']:
                    name = key[:-1]+tag 
                    for each_data in [overlap_3_network,overlap_5_network]:
                        if name in each_data:
                            del each_data[ key[:-1]+tag  ]
                continue	
        for key in cache:
            all_best_reads_need[ key[:-1]  ] = ''
        seqeunce =  subprocess.check_output( shlex.split( PATH+'tigStore -g %s -t %s 3 -d consensus -u %s '%( gkp,tig,each_unitig  )  ) )
        s = re.sub( '\s+','',seqeunce.split('\n',1)[-1] )

        all_unitig_data [ each_unitig ]=[len( s ),s     ]
        head_unitig[ each_unitig ] = cache[0]
        tail_unitig[ each_unitig  ] = cache[-1]
        TRIM_CACHE_READS = open( 'trim_cache_reads%s.fasta'%(each_unitig),'w' )
        TRIM_CACHE_UNITIG = open( 'trim_cache_unitig%s.fasta'%( each_unitig ),'w'  )
        TRIM_CACHE_READS.write( '>head\n'+all_reads[ cache[0][:-1] ] )
        TRIM_CACHE_READS.write( '>tail\n'+all_reads[ cache[-1][:-1] ] )
        TRIM_CACHE_UNITIG.write( '>%s\n'%( each_unitig )+all_unitig_data[  each_unitig  ][ -1  ]   )
        TRIM_CACHE_READS.close()
        TRIM_CACHE_UNITIG.close()
        os.system( 'nucmer --maxmatch  %(unitig)s  %(read)s  -p trim >/dev/null 2>&1' %( {  
            'unitig':TRIM_CACHE_UNITIG.name  ,
            'read':TRIM_CACHE_READS.name
        }  )   )
        nucmer_out = subprocess.check_output(  shlex.split('show-tiling -a -R trim.delta' )  )

        for line in nucmer_out.split('\n'):
            if not line:
                continue
            line_l = line.strip().split( '\t' )

            start,end = int( line_l[0]),int( line_l[1]) 
            if line_l[-1] =='head':
                trim_start = start
                trim_end = end
            else:
                trim_end = end

        new_seq = all_unitig_data[  each_unitig  ][ -1  ][ trim_start:trim_end   ]
        all_unitig_data[  each_unitig  ] = [len(new_seq),new_seq ]
        if len(cache)==1:
            every_contig_detail[ each_unitig ][ cache[0]  ] = ''
            continue
        for each_index in xrange( 1,len( cache ) ):
            unitig_graph_3[ cache [each_index-1]   ][ cache [each_index ]   ] = ''
            every_contig_detail[ each_unitig ][ cache [each_index-1]   ][ cache [each_index ]   ] = ''
        every_contig_detail[ each_unitig ][ cache [-1]   ][ ''   ] = ''
        for each_index in xrange( 1,len( cache ) ):
            unitig_graph_5[ cache [each_index]   ][ cache [each_index-1 ]   ] = ''		

    END = open( best,'w' )
    for key in all_best_reads_need:
        END.write( '>%s\n%s'%(  key,all_reads[key]    )  )


    #开始比较两个图的差异
    all_different = {}
    different_5 = {}
    different_3 = {}
    TURE_UNIQUE = open( 'unitig.fasta','w' )


    for key in unitig_graph_3:
        if overlap_3_network[key]!= unitig_graph_3[key] :

            all_different[  key[:-1]  ] = ''
            different_3[ key  ] = ''
    for key in unitig_graph_5:		
        if overlap_5_network[key]!= unitig_graph_5[key]:

            all_different[  key[:-1] ] = ''
            different_5[ key ] = ''


    #记录unitig打断的坐标
    #并打入split_cache这个列表中，列表的值为[ 上一个的断点，下一个的起点],[上次的终点reads名，下次的起点reads名     ]
    #true_unitig_seq记录每个unitig的序列
    true_unitig_3 = {}
    true_unitig_5 = {}
    true_unitig_seq = {}
    #########################################

    for utgs in sorted(  every_contig_detail ,key=lambda x: int(x) ):

        split_cache = []
        has_checked = {}
        i=0
        CACHE_READS = open( 'cache_reads.fasta','w' )
        CACHE_UNITIG = open( 'cache_unitig.fasta','w'  )

        for each_data in  every_contig_detail[ utgs]:
            if each_data[:-1] in all_different:
                i=1
                CACHE_READS.write( '>%s\n%s'%( each_data[:-1] , all_reads[ each_data[:-1] ])  )
        if i==1:
            CACHE_UNITIG.write( '>%s\n%s'%(  'utg'+utgs , all_unitig_data[ utgs  ][-1]  )  )
            CACHE_UNITIG.close()
            CACHE_READS.close()
            os.system( 'nucmer --maxmatch cache_unitig.fasta cache_reads.fasta -p cache >/dev/null 2>&1 '     )
            nucmer_out = subprocess.check_output(  shlex.split('show-coords -cT cache.delta' )  )
            nucmer_out = get_nucmer_best( nucmer_out )
            for node,[ start,end  ] in nucmer_out:
                status = []

                if node in different_3:
                    junction_3 = max( start,end )
                    status.append( '3')
                if node in different_5:
                    status.append( '5' )

                    junction_5 = min( start,end )

                if ['5'] == status and not  unitig_graph_5[ node ]: 
                    continue

                elif node in unitig_graph_5 and '5' in status:

                    CACHE_READS2 = open( 'cache2_reads.fasta','w' )
                    CACHE_READS2.write( '>%s\n%s'%( unitig_graph_5[ node  ].keys()[0][:-1], all_reads[ unitig_graph_5[ node  ].keys()[0][:-1] ])  )
                    #CACHE_READS2.close()

                    os.system( 'nucmer --maxmatch cache_unitig.fasta cache2_reads.fasta -p cache2 >/dev/null 2>&1'     )
                    nucmer_out = subprocess.check_output(  shlex.split('show-coords -cT cache2.delta' )  )
                    nucmer_out = get_nucmer_best(   nucmer_out )
                    other_end = nucmer_out[0][1][1]					

                    node_cache = unitig_graph_5[node].keys()[0]+'\t'+node
                    if node_cache not in has_checked:
                        has_checked[  node_cache ] = ''

                        split_cache.append( [[ other_end, junction_5  ],[ unitig_graph_5[node].keys()[0],node    ]]   )

                if status==['3'] and node not in unitig_graph_3: 
                    continue
                elif node in unitig_graph_3 and '3' in  status:

                    CACHE_READS2 = open( 'cache2_reads.fasta','w' )
                    CACHE_READS2.write( '>%s\n%s'%( unitig_graph_3[ node  ].keys()[0][:-1], all_reads[ unitig_graph_3[ node  ].keys()[0][:-1] ])  )
                    os.system( 'nucmer --maxmatch cache_unitig.fasta cache2_reads.fasta -p cache2 >/dev/null 2>&1'     )
                    nucmer_out = subprocess.check_output(  shlex.split('show-coords -cT  cache2.delta' )  )
                    nucmer_out = get_nucmer_best(   nucmer_out )
                    other_end = nucmer_out[0][1][0]
                    node_cache = node+'\t'+unitig_graph_3[node].keys()[0]
                    if node_cache not in has_checked:
                        has_checked[ node_cache ] = ''
                        split_cache.append( [ [ other_end, junction_3  ] ,[node,unitig_graph_3[node].keys()[0]]  ]  )


        k=0	

        if 	split_cache:
            start = head_unitig[ utgs  ]

            if len( split_cache )==1:
                name = utgs+'_'+str( k ) 
                TURE_UNIQUE.write( '>%s\n'%( name  )+re.sub('(\w{60})','\\1\n',all_unitig_data[utgs][-1][   :max( split_cache[0][0]  )  ]) +'\n' )

                true_unitig_seq[ name+'+'  ] = all_unitig_data[utgs][-1][   
                    :max( split_cache[0][0]  )  
                ]

                true_unitig_3[ name+'+'  ] = split_cache[0][1][0]
                true_unitig_3[ name+'-'  ] = start.translate( libary )
                true_unitig_5[ name+'+'  ] = start
                true_unitig_5[ name+'-'  ] = split_cache[0][1][0].translate( libary )
                start =split_cache[0][1][1]
                k+=1
                name = utgs+'_'+str( k ) 
                true_unitig_5[ name+'+'  ] = start
                true_unitig_5[ name+'-'  ] = tail_unitig[ utgs ].translate( libary )
                true_unitig_3[ name+'+'  ] = tail_unitig[ utgs ]
                true_unitig_3[ name+'-'  ] = start.translate( libary )				
                TURE_UNIQUE.write( '>%s\n'%( name )+re.sub( '(\w{60})','\\1\n' , all_unitig_data[utgs][-1][   min( split_cache[0][0]  ):  ] )+'\n' )

                true_unitig_seq[ name+'+'  ] = all_unitig_data[utgs][-1][   min( split_cache[0][0]  ):  ] 
            else:	
                for j in xrange( 0,len( split_cache ) ):
                    name = utgs+'_'+str( j ) 


                    if j==0:
                        start = head_unitig[ utgs  ]
                        tail = tail_unitig[ utgs  ]					
                        TURE_UNIQUE.write( '>%s\n'%( utgs+'_'+str( j )  )+re.sub('(\w{60})','\\1\n',all_unitig_data[utgs][-1][   :max( split_cache[j][0]  )  ])  +'\n' )

                        true_unitig_seq[ utgs+'_'+str( j )+'+'  ] = all_unitig_data[utgs][-1][   :max( split_cache[j][0]  )  ]
                        next_start = min( split_cache[j][0]  )
                        true_unitig_3[ name+'+'  ] = split_cache[j][1][0]
                        true_unitig_3[ name+'-'  ] = start.translate( libary )
                        true_unitig_5[ name+'+'  ] = start

                        true_unitig_5[ name+'-'  ] = split_cache[j][1][0].translate( libary )					
                        start =split_cache[j][1][1]


                    else:

                        TURE_UNIQUE.write( '>%s\n'%( utgs+'_'+str( j )  )+re.sub('(\w{60})','\\1\n',all_unitig_data[utgs][-1][ next_start:  max( split_cache[j][0]  ) ])  +'\n'  )

                        true_unitig_seq[ utgs+'_'+str( j )+'+'  ] = all_unitig_data[utgs][-1][
                            next_start:  max( split_cache[j][0]  ) 
                        ]

                        next_start = min( split_cache[j] [0] )
                        true_unitig_5[ name+'+'  ] = start
                        true_unitig_5[ name+'-'  ] = split_cache[j][1][0].translate( libary )
                        true_unitig_3[ name+'+'  ] = split_cache[j][1][0]
                        true_unitig_3[ name+'-'  ] = start.translate( libary )					
                        start =split_cache[j][1][1]

                else:
                    name =  utgs+'_'+str( j+1 )
                    TURE_UNIQUE.write( '>%s\n'%( utgs+'_'+str( j+1 )  )+re.sub('(\w{60})','\\1\n',all_unitig_data[utgs][-1][   min( split_cache[j][0]  ) : ])  +'\n' )

                    true_unitig_seq[ utgs+'_'+str( j+1 )+'+'  ] = all_unitig_data[utgs][-1][
                        min( split_cache[j][0]  ) : 
                    ]				
                    true_unitig_5[ name+'+'  ] = start
                    true_unitig_5[ name+'-'  ] = tail.translate( libary )
                    true_unitig_3[ name+'+'  ] = tail
                    true_unitig_3[ name+'-'  ] = start.translate( libary )				
        else:
            true_unitig_5[ utgs+'+'  ] = head_unitig[ utgs ]
            true_unitig_5[ utgs+'-'  ] = tail_unitig[ utgs ].translate( libary )
            true_unitig_3[ utgs+'+'  ] = tail_unitig[ utgs ]
            true_unitig_3[ utgs+'-'  ] = head_unitig[ utgs ].translate( libary ) 		
            TURE_UNIQUE.write( '>%s\n'%( utgs )+re.sub( '(\w{60})','\\1\n', all_unitig_data[utgs][-1])+'\n' )

            true_unitig_seq[ utgs  ] = all_unitig_data[utgs][-1]	

    for key in sorted(true_unitig_5,key=lambda x: int( re.search( '(\d+)',x ).group(1)  )):
        OUTPUT.write( key +'\t'+true_unitig_5[key]+'\t'+true_unitig_3[key]+'\n' )
