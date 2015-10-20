#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/7/9


from lpp import *
libary=string.maketrans('+-','-+')
#将best.edges的数据打入内存
overlap_3_network =Ddict()
overlap_5_network = Ddict()

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
for line in open( sys.argv[1],'rU'):
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

data = sys.argv[2]
print( '3   '  )
print( overlap_3_network[data]  )
print('5')
print( overlap_5_network[data]  )
