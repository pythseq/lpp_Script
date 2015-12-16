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
def rmerge(left,right,**kwargs):
    """Perform a merge using pandas with optional removal of overlapping
    column names not associated with the join. 

    Though I suspect this does not adhere to the spirit of pandas merge 
    command, I find it useful because re-executing IPython notebook cells 
    containing a merge command does not result in the replacement of existing
    columns if the name of the resulting DataFrame is the same as one of the
    two merged DataFrames, i.e. data = pa.merge(data,new_dataframe). I prefer
    this command over pandas df.combine_first() method because it has more
    flexible join options.

    The column removal is controlled by the 'replace' flag which is 
    'left' (default) or 'right' to remove overlapping columns in either the 
    left or right DataFrame. If 'replace' is set to None, the default
    pandas behavior will be used. All other parameters are the same 
    as pandas merge command.

    Examples
    --------
    >>> left       >>> right
       a  b   c       a  c   d 
    0  1  4   9    0  1  7  13
    1  2  5  10    1  2  8  14
    2  3  6  11    2  3  9  15
    3  4  7  12    

    >>> rmerge(left,right,on='a')
       a  b  c   d
    0  1  4  7  13
    1  2  5  8  14
    2  3  6  9  15
    >>> rmerge(left,right,on='a',how='left')
       a  b   c   d
    0  1  4   7  13
    1  2  5   8  14
    2  3  6   9  15
    3  4  7 NaN NaN
    >>> rmerge(left,right,on='a',how='left',replace='right')
       a  b   c   d
    0  1  4   9  13
    1  2  5  10  14
    2  3  6  11  15
    3  4  7  12 NaN

    >>> rmerge(left,right,on='a',how='left',replace=None)
       a  b  c_x  c_y   d
    0  1  4    9    7  13
    1  2  5   10    8  14
    2  3  6   11    9  15
    3  4  7   12  NaN NaN
    """

    # Function to flatten lists from http://rosettacode.org/wiki/Flatten_a_list#Python
    def flatten(lst):
        return sum( ([x] if not isinstance(x, list) else flatten(x) for x in lst), [] )

    # Set default for removing overlapping columns in "left" to be true
    myargs = {'replace':'left'}
    myargs.update(kwargs)

    # Remove the replace key from the argument dict to be sent to
    # pandas merge command
    kwargs = {k:v for k,v in myargs.iteritems() if k is not 'replace'}

    if myargs['replace'] is not None:
        # Generate a list of overlapping column names not associated with the join
        skipcols = set(flatten([v for k, v in myargs.iteritems() if k in ['on','left_on','right_on']]))
        leftcols = set(left.columns)
        rightcols = set(right.columns)
        dropcols = list((leftcols & rightcols).difference(skipcols))

        # Remove the overlapping column names from the appropriate DataFrame
        if myargs['replace'].lower() == 'left':
            left = left.copy().drop(dropcols,axis=1)
        elif myargs['replace'].lower() == 'right':
            right = right.copy().drop(dropcols,axis=1)

    df = pd.merge(left,right,**kwargs)

    return df






def combine_xls( data_list   ):
    out_frame = pd.read_table(data_list[0])

    for each_data in data_list[1:]:
        out_frame = rmerge(out_frame, pd.read_table(each_data),on="Name",how="outer")
        # out_frame = pd.DataFrame.merge(out_frame, pd.read_table(each_data), left_on='Name', right_on='Name', how='right')
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
    parser.add_option("-g", "--GFFANNO", action="store", 
                      dest="gff", 
                      default="",
                      help="Annotation from gff file")	    



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
    STAT = open(category_dir+'/stat.tsv','w')
    STAT.write("Database\tHitGeneNumber\n")
    total_excel = []
    database_data  = {}
    for category in category_hash:
        all_excel = []
        
        for chrosome in category_hash[category]:
            all_excel.append(  category_hash[category][chrosome]  )
        total_excel.extend(all_excel)
        result_frame = combine_xls(all_excel)
        
        STAT.write(category+'\t%s\n'%(len(result_frame["Name"] ) ) )
        
        result_frame["from"] = result_frame["Name"].str.split('_',1).str.get(0)
        
        result_frame["id"] = result_frame["Name"].str.split('_',1).str.get(1)
        result_frame =result_frame.sort(["from",'id'],axis=0)
        result_frame = result_frame.drop(["from",'id'],axis=1)
        
        result_frame.to_excel( category_Excel,category ,index=False   )
        if category!="Nt":
            database_data[category] = result_frame["Name"]
    category_Excel.save()
    VENN_R = open( category_dir+"/Draw.R",'w'   )
    VENN_R.write(
        """
require("VennDiagram")
temp = venn.diagram(
     x = list(
 
        """)
    
    
    
    end_list = []
    for category ,data in database_data.items():
        end_list.append(  """    %s=c(%s)
        
"""%(
    category,
    ','.join(["'"+x+"'"  for x in data])
    
   
   )
   )
    VENN_R.write(",".join(end_list))

    VENN_R.write("""),
    filename = NULL,
	col = "black",
	lty = "solid",
	lwd = 4,
	fill = c("cornflowerblue", "green", "yellow", "darkorchid1"),
	alpha = 0.50,
	label.col = c("orange", "white", "darkorchid4", "white", "white", "white", "white", "white", "darkblue", "white", "white", "white", "white", "darkgreen", "white"),
	cex = 2.5,
	fontfamily = "serif",
	fontface = "bold",
	cat.col = c("darkblue", "darkgreen", "orange", "darkorchid4"),
	cat.cex = 2.5,
	cat.fontfamily = "serif"
	)    
pdf("%s")
grid.draw(temp)    
dev.off()    
    """%(
           category_dir+'/stat.pdf'
           
       
       )
       
       
       )
    VENN_R.close()
    os.system("Rscript %s "%( VENN_R.name  ))
    
    
    chrosome_Excel = pd.ExcelWriter(chrosome_dir+'ChorosomeAnnotation.xlsx', engine='xlsxwriter')
    
    for chrosome in chrosome_hash:
        all_excel = []
        for category in chrosome_hash[chrosome]:
            all_excel.append(  category_hash[category][chrosome]  )
        
        result_frame = combine_xls(all_excel)
        result_frame["from"] = result_frame["Name"].str.split('_',1).str.get(0)
    
        result_frame["id"] = result_frame["Name"].str.split('_',1).str.get(1)
        result_frame =result_frame.sort(["from",'id'],axis=0)
        result_frame = result_frame.drop(["from",'id'],axis=1)        
        result_frame.to_excel( chrosome_Excel,chrosome,index=False    )
    chrosome_Excel.save()
    
    all_resultframe = combine_xls(total_excel)
    STAT.write("Total\t%s\n"%(len(all_resultframe)))
    
    all_resultframe["from"] = all_resultframe["Name"].str.split('_',1).str.get(0)
    all_resultframe["id"] = all_resultframe["Name"].str.split('_',1).str.get(1)
    all_resultframe =all_resultframe.sort(["from",'id'],axis=0)
    all_resultframe = all_resultframe.drop(["from",'id'],axis=1)    
    all_resultframe.to_excel( out_put_path+"All_HasAnnotation.xls" ,index=False   )
    
    if options.gff:
        all_gff_frame= pd.read_table( options.gff  )
        total_resultframe = pd.DataFrame.merge(all_gff_frame, all_resultframe, left_on='Name', right_on='Name', how='outer')
        total_resultframe.to_csv(out_put_path+"GeneFeature+Annotation.xlsx",index=False,sep="\t"   )
    
    
    

    