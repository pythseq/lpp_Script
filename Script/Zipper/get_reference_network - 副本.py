#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/7/5


from lpp import *
from optparse import OptionParser
import subprocess,shlex
from configure import cele_path
libary=string.maketrans('+-','-+')

#将best.edges的数据打入内存
overlap_3_network =Ddict()
overlap_5_network = Ddict()

def Get_reference_network(  FILE  ):
    #读参考图文件并生成来两个图，分别记录5‘方向和3’方向
    return3_ref = Ddict()
    return5_ref = Ddict()
    name = {}
    all_chr= []
    all_ref = []
    for line in FILE:

        line_l =line.strip().split('\t')
        name_2,reads = line_l
        if name_2 not in name:
            if len(  name ):
                all_chr.append( all_ref  )
                name[ name_2 ] = ''
                all_ref = []
        #判断上下游是否在reference上，都不在的话，跳过！
        i=0;j=0
        if reads in overlap_3_network:
            for read3 in overlap_3_network[reads]:
                if  read3[:-1] in reads_in_reference:
                    i=1
                    break
        else:
            i=1
        if reads in overlap_5_network:
            for read5 in overlap_5_network[reads]:
                if  read5[:-1] in reads_in_reference:
                    j=1
                    break 
        else:
            j=1
        if i==0 and j==0:
            continue
        all_ref.append( reads  )
    else:
        all_chr.append( all_ref  )        
    for each_chr in all_chr:	
        for i in xrange( 0,len(each_chr)-1 ):   
            return3_ref[   each_chr[i]    ][   each_chr[i+1 ]   ] = ''
            return3_ref[  each_chr[i+1 ].translate( libary )     ][  each_chr[i].translate( libary )    ] = ''
        for i in xrange( 1,len(each_chr) ):
            return5_ref[   each_chr[i]    ][   each_chr[i-1 ]   ] = ''
            return5_ref[   each_chr[i-1   ].translate( libary )     ][  each_chr[i].translate( libary )    ]
    return return3_ref, return5_ref





def change_network( network,node1, node2,network2   ):
    #如果督导图和overlap图都存在的话，用督导图的唯一关系替代overlap图中的多维关系
    if node1 =='1252-':
        print(  node2 )    
    if node1 in network and node2 in network[node1]:
        
        for key1 in network[node1]:

            network2[ key1  ][ node1 ]=''
            del network2[ key1  ][ node1 ]
        del network[node1]
        network[node1][node2] = ''
        network2[node2][node1] = ''

    elif node1[:-1] in  all_doubt or node2[:-1] in all_doubt:
        
        #使用overlap_check.py查询两个reads是否具有overlap，如果是肯定的，则会对整个的图进行修改
        data = subprocess.check_output( shlex.split( cele_path+'/overlap_check.py  -g %s -s %s -q %s    ' %(  overlapStore, node1[:-1],node2[:-1]  )      )    )

        if data:

            if network==overlap_3_network:
                node1,node2 = data.split()
                
            else:
                node2,node1 = data.split()
            
            for each_nd in [ [node1,node2],[node2.translate( libary ),node1.translate( libary )  ] ]:
                
                for key1 in network[each_nd[0]  ] :
                    network2[  key1   ][each_nd[0]  ] = ''
                    del network2[  key1   ][each_nd[0]  ]
                del network[each_nd [0] ]
                network[ each_nd[0]  ][  each_nd[1]   ] = ''
                network2[  each_nd[1]   ] [  each_nd[0]   ]  = ''




def get_para(   ):
    #获得运行参数
    usage = '''
	%prog [ options ]
	'''
    parser = OptionParser( usage = usage  )


    parser.add_option("-u","--UNI",action= "store",
                      dest = "uni",
                      help="Unitig Path contained best.edges file"
                      )

    parser.add_option("-g","--GRAPH",action= "store",
                      dest = "graph",
                      help="Unitig graph generated by celera_zipper"
                      )

    parser.add_option("-c","--REF",action= "store",
                      dest = "reference",
                      help="Reference graph generated by celera_blat"
                      )	
    parser.add_option("-o","--OUTPUT",action= "store",
                      dest = "output",
                      help="Output File"
                      )	
    parser.add_option("-v","--OVERLAP",action= "store",
                      dest = "overlap",
                      help="OverlapStore"
                      )		

    (options, args) = parser.parse_args()
    return options,args

if __name__=='__main__':
    #获得参数
    options,args = get_para()
    overlapStore = options.overlap
    RAW = open( options.reference,'rU' )
    #将所有在reference上存在的reads名记录下来
    RAW2 = open( options.reference,'rU' ) 
    reads_in_reference = {}
    for line in RAW2:
        
        name = line.strip().split('\t')[-1][:-1]
       
        reads_in_reference[  name   ] = ''
    
    
    
    
    
    


    
    #进行overlap图创建，整合后这部分代码删除
    def get_value( data ):
        global overlap_3_network,overlap_5_network
        for i in xrange(0,len(data)-1):
            if data[i][0] =='0' or data[i+1][0] =='0':
                continue
            overlap_3_network[ data[i] ][ data[i+1] ] = ''
        for i in xrange( 1,len( data )  ):
            if data[i][0] =='0' or data[i-1][0] =='0':
                continue		
            overlap_5_network[ data[i] ] [ data[i-1]  ] = ''	
    for line in open( options.uni+'best.edges','rU'):
        if '#' in line:
            continue
        data = []
        line_l = line[:-1].split('\t')
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

    #摄取reference的比对结果并与unitig的结果进行验证，然后对不同的unitig进行排序和整合
    #读取untig的情况
    RAW_2 = open( options.graph,'rU' )
     
    true_unitig_5 = {}
    true_unitig_3 = {}
    rela_5 = {}
    rela_3 = {}
    all_doubt = {}
    all_node = {}
    for line in RAW_2:
        line_l = line.strip().split('\t')
        name = line_l[0]
        all_node[  name[:-1]  ] = ''
        rela_5[ line_l[1] ] = name
        true_unitig_5[  name   ] = line_l[1]
        true_unitig_3[ name  ] = line_l[-1]
        rela_3[ line_l[-1] ] = name
        
    for key1 in rela_3:
        all_doubt[ key1[:-1] ] = ''
        
    for key2 in rela_5:
        all_doubt[ key2[:-1] ] = ''
    
    already = {}

    #根据督导图对overlap图进行更迭 overlapStore是overlap store 文件夹的位置

    ##载入参考图
    refer3_network,refer5_network= Get_reference_network( RAW   ) 
    for key1 in refer3_network:
        for key2 in refer3_network[key1]:
            change_network(  overlap_3_network, key1, key2 ,overlap_5_network   )
        
    for key1 in refer5_network:
        for key2 in refer5_network[key1]:
            change_network(  overlap_5_network, key1, key2  ,overlap_3_network  )

    END = open( options.output,'w' )

    for each_node in all_node:
        if each_node in already:
            continue
        node = each_node+'+'
        #判断是否为自成环质粒
        if node[:-1] not in already and true_unitig_5[ node ]  in overlap_5_network  and  len(    overlap_5_network[   true_unitig_5[ node ]   ]   )==1  and  overlap_5_network[   true_unitig_5[ node ]   ].keys()[0]  in    rela_3 and rela_3[  overlap_5_network[   true_unitig_5[ node ]   ].keys()[0]   ] ==node :
            END.write( 'Plasmid !!\t'+node+'\n'  )
            already[ node[:-1] ] = ''
            continue	

        has=[ node ]


        node_raw = node
        
        #用overlap图单向延伸5’方向
        while node[:-1] not in already and true_unitig_5[ node ]  in overlap_5_network  and  len(    overlap_5_network[   true_unitig_5[ node ]   ]   )==1  and  overlap_5_network[   true_unitig_5[ node ]   ].keys()[0]  in    rela_3 and len(   overlap_3_network [  overlap_5_network[   true_unitig_5[ node ]   ].keys()[0]   ]   )==1:
            cache = rela_3[      overlap_5_network [   true_unitig_5[ node ]     ].keys()[0]    ]

            if cache[:-1] in already:
                break		
            has.insert( 0, cache )
            if node_raw  != node:
                already[ node[:-1]  ] = ''
            node = cache
        if node_raw!=node:
            already[ node[:-1]   ] = ''	
        #用reference图和伸3‘方向
        node = node_raw

        while node[:-1] not in already and true_unitig_3[ node ]  in overlap_3_network  and  len(    overlap_3_network[   true_unitig_3[ node ]   ].keys()   )==1  and  overlap_3_network[   true_unitig_3[ node ]   ].keys()[0]  in    rela_5 and  len(    overlap_5_network[  overlap_3_network[   true_unitig_3[ node ]   ].keys()[0]  ]   )==1:

            cache = rela_5[      overlap_3_network [   true_unitig_3[ node ]     ].keys()[0]    ]
            if cache[:-1] in already:
                break
            has.append(  cache )

            already[ node[:-1]  ] = ''
            node = cache			
        already[ node[:-1]   ] = ''	


        #寻找overlap关系图中唯一的关系

        END.write('\t'.join(has)+'\n')
#for key1 in  refer3_network:
    #for key2 in refer3_network[key1]:
        #print( key1+'\t'+key2 )
