#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/12/6
"""
from Dependcy import *
from optparse import OptionParser
import os,string

def combine_xls( data_list   ):
    out_frame = pd.read_table(data_list[0])
    for each_data in data_list[1:]:
        out_frame = pd.DataFrame.merge(out_frame, pd.read_table(each_data), left_on='Name', right_on='Name', how='outer')
    return out_frame


if __name__=="__main__":
    config_hash = Config_Parse()

    usage = '''usage: python2.7 %prog'''
    parser = OptionParser(usage =usage ) 
    
    parser.add_option("-i", "--inputpath", action="store", 
                      dest="inputpath", 
                      default = "./",
                      help="input path")
    parser.add_option("-o", "--outPath", action="store", 
                      dest="outputpath", 
                      help="outpath")		



    (options, args) = parser.parse_args() 

    out_put_path = os.path.abspath(  options.outputpath )

    if not os.path.exists( out_put_path ):
        os.makedirs( out_put_path )
    README = open(out_put_path+"/Readme.txt",'w')
    README.write(
"""
该文件夹放置所有注释分析的表格，分成两类，第一类是按照不同的数据库进行分类，每一个子文件夹放置的excel文件包含该数据库下所有样本的注释结果。第二类是按照样本来源分类，每一个子文件夹下放置不同染色体的基因注释信息附件说明如下：
Database文件夹\t不同数据库注释的汇总文件
Choromsome文件夹\t按照不同染色体进行的分类汇总文件
Total文件夹\t所有注释信息汇总在一起的结果



""")
    category_hash = Ddict()
    chrosome_hash = Ddict()
    for base_path,dir_name,file_list in os.walk(options.inputpath):
        for e_f in file_list:
            if e_f.endswith(".xls"):
                chrosmome,category=  base_path.rsplit('/',2)[-2:]
                category_hash[category][chrosmome] = base_path+'/'+e_f
                chrosome_hash[chrosmome][category] = base_path+'/'+e_f
                
    chrosome_dir = out_put_path+"/Choromsome/"
    category_dir = out_put_path+"/Database/"
    for e_path in [ chrosome_dir, category_dir  ]:
        if not os.path.exists(e_path):
            os.makedirs(e_path)
            
    category_Excel = pd.ExcelWriter(category_dir+'CategoryAnnotation.xlsx', engine='xlsxwriter')
    total_excel = []
    for category in category_hash:
        all_excel = []
        for chrosome in category_hash[category]:
            all_excel.append(  category_hash[category][chrosome]  )
        total_excel.extend(all_excel)
        result_frame = combine_xls(all_excel)
        
        
        result_frame["from"] = string.rsplit( result_frame["Name"].astype("string"),"_",1  )[0]
        print(result_frame["from"])
        result_frame["id"] = string.rsplit( result_frame["Name"].astype("string"),"_",1  )[1]
        result_frame =result_frame.sort(["from",'id'],axis=1)
        result_frame = result_frame.drop(["from",'id'],axis=1)
        
        result_frame.to_excel( category_Excel,category   )
        
    category_Excel.save()

    chrosome_Excel = pd.ExcelWriter(chrosome_dir+'ChorosomeAnnotation.xlsx', engine='xlsxwriter')
    
    for chrosome in chrosome_hash:
        all_excel = []
        for category in chrosome_hash[chrosome]:
            all_excel.append(  category_hash[category][chrosome]  )
        
        result_frame = combine_xls(all_excel)
        result_frame.to_excel( chrosome_Excel,chrosome   )
    chrosome_Excel.save()
    
    all_resultframe = combine_xls(total_excel)
    all_resultframe.to_excel( out_put_path+"AnnotationAll.xls"   )
    
    
    
    

    