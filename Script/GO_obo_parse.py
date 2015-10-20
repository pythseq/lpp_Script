#!/usr/bin/env python
#coding:utf-8
# Author:  LPP --<lpp1985@hotmail.com>
# Purpose: 
# Created: 2011/5/26
from lpp import *
RAW = block_reading(  open( sys.argv[1],'rU'   ) ,tag='^\[\S+\]'       )
IS_A = open( 'relationship.son','w'  )
NAME_DEF = open( 'NAME_DEF.list','w' )
PART_OF = open( 'relationship.belong','w'  )
root = {}
ALTER = open( 'relationship.alter','w'   )
leaf_2 = {}
leaf_3 = {}

	
for e_b in RAW:
	if  e_b .startswith('id: GO:'):
		go_id = re.search( '^id\: (GO\:\d+)',e_b ).group(1)
		alter_all = re.findall( 'alt_id\: (\S+)',e_b )
		for each_altered in alter_all:
			ALTER.write( each_altered+'\t'+go_id+'\n' )
		consider_all = re.findall( 'consider\: (\S+)',e_b )
		for each_consider in consider_all:
			ALTER.write( go_id+'\t'+each_consider+'\n' )
			
			
		if 'is_obsolete: true' in e_b:
			replace_by = re.findall("replaced_by\: (\S+)",e_b)
			for replace in replace_by:
				ALTER.write( go_id+'\t'+replace+'\n' )
			continue
		go_id = re.search( '^id\: (GO\:\d+)',e_b ).group(1)
		name = re.search( '\nname\: (.+)\n',e_b  ).group(1)
		define = re.search(  'def\: (.+)',e_b )
		if not define:
			define = ""
		else:
			define = define.group(1)
		NAME_DEF.write( go_id+'\t'+name+'\t'+define+'\n'    )
		all_father = re.findall( 'is_a\: (GO\:\d+)',e_b )
		for each_father in all_father:
			IS_A.write( each_father+'\t'+go_id+'\n' )
		if not all_father:
			root[ go_id ] = ''
		part_of = re.findall('relationship\: part_of (\S+)',e_b)
		for each_comp in part_of:
			PART_OF.write(each_comp+'\t'+go_id+'\n'   )
		
all_sonR = File_Ddict(  open( IS_A.name,'rU'  )  ).read(1,2)
for each_key1 in root:
	for each_key2 in all_sonR[ each_key1  ]:
		leaf_2[ each_key2 ] = ''
		for each_key3 in all_sonR[ each_key2  ]:
			leaf_3 [ each_key3 ] = ''
ALL_FAT = open( 'ROOT.root','w'  )
for key1 in root:
	ALL_FAT.write( key1+'\t1\n'  )
for key2 in leaf_2:
	ALL_FAT.write( key2+'\t2\n'  )
#for key3 in leaf_3:
	#ALL_FAT.write( key3+'\t3\n'  )	
