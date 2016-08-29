from Dependcy import *
from optparse import OptionParser
import os,string
def Rawcombine_xls( data_list   ):
    out_frame = data_list[0].drop_duplicates()

    for new_frame in data_list[1:]:

        on_need = list(out_frame.columns  & new_frame.columns)

        out_frame = pd.DataFrame.merge(out_frame, new_frame, on=on_need, how='outer')
    return out_frame.drop_duplicates()


if __name__=="__main__":
    all_File_list = sys.argv[1:-1]
    all_result = Rawcombine_xls(all_File_list)
    all_result.to_csv(sys.argv[-1],index=False,sep="\t")