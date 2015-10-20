#!/usr/bin/python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 2013/8/28


from lpp import *
import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
#进行overlap图创建，整合后这部分代码删除


	
DATA = open( sys.argv[1],'rU'  )

for line in DATA:
	line_l = line.strip().split('\t')
	data = ''
	for key in line_l:
		G.add_node(  key )
		if  data:
			G.add_edge( data,key )
		data = key
		
pos = nx.spring_layout( G )
nx.draw_networkx_nodes(G,pos,node_size=600)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos,font_size=13,font_family='sans-serif',alpha =10)
plt.axis('off')
plt.savefig(sys.argv[2]) # save as png
plt.show() # display
