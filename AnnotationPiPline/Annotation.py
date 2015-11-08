#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LPP --<Lpp1985@hotmail.com>
  Purpose: 
  Created: 2015/1/2
"""
from Lib.Dependcy import *
from termcolor import colored
import time
import os
from optparse import OptionParser
from pyflow import WorkflowRunner

usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--Sequence", action="store",
                  dest="Sequence",

                  help="Contig")
parser.add_option("-o", "--Output", action="store",
                  dest="Output",

                  help="OutputPath")
parser.add_option("-c", "--Config", action="store",
                  dest="Config",

                  help="Config File")

class Ghostz(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value):
        self.Input = Input
        self.Output = Output
        self.Database = Database
        self.E_value = E_value
    def workflow(self):
        print("%s is start to blast to %s"%(self.Input,self.Database))
        blast_out = self.Output
        self.addTask("Blast","nohup "+scripts_path +"ghostz_continue.py -i %s -o %s -e %s -d %s "%(
            self.Input,
            blast_out,
            self.E_value,
            self.Database,

        )
                     )
        
        
class Blast(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value):
        self.Input = Input
        self.Output = Output
        self.Cache = self.Output.rsplit(".",1)[0]+'.cache'
        self.Database = Database
        self.E_value = E_value
    def workflow(self):
        print("%s is start to blast to %s"%(self.Input,self.Database))

        self.addTask("Blast","  blastn -query %i -db %s -num_threads 64 -max_target_seqs 1 -evalue %s -outfmt 5 -out %s &&blast_parse.py %s "%(
            self.Input,
            self.Database,
            self.E_value, 
            self.Cache,
            self.Cache

        )
                    )




class Nr_Mapping(Blast):
    def __init__(self,Input,Output):
        self.Input = Input
        self.Output = Output
        self.Database = config_hash["Database"]["nr"]
        self.E_value = config_hash["Threshold"]["e_value"]
        self.Total_Database = os.path.split( self.Input)[0]+"/../../total.db" 
    def workflow(self):
        print(
            colored(
                "%s's Nr Result is Running"%(self.Input),
                "red"
            )
        )       

        blast_flow = Ghostz(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)
        self.addTask("Database",
                     "nohup "+scripts_path+'/Nr_Database.py %s %s '%(
                         self.Total_Database,
                         self.Output
                         ),
                     dependencies="Blast"

                     )        
class Nt_Mapping(Blast):
    def __init__(self,Input,Output):
        self.Input = Input
        if not Output.endswith(".Bparse"):
            Output = Output+".Bparse"
        self.Output = Output
        self.Database = config_hash["Database"]["nt"]
        self.E_value = config_hash["Threshold"]["e_value"]
        self.Total_Database = os.path.split( self.Input)[0]+"/../../total.db" 
    def workflow(self):
        print(
            colored(
                "%s's Nr Result is Running"%(self.Input),
                "red"
            )
        )       

        blast_flow = Blast(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)
        self.addTask("Database",
                     "nohup "+scripts_path+'/Nr_Database.py %s %s '%(
                         self.Total_Database,
                         self.Output
                         ),
                     dependencies="Blast"

                     )        




class COG_Mapping(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value,Total_Database):
        self.Input = Input
        self.Output = Output
        self.Database = Database
        self.E_value = E_value
        self.Total_Database = Total_Database
        self.COG = config_hash["Taxon"]["COG"]

    def workflow(self):
        print(
            colored(
                "%s's Cog Result is Running"%(self.Input),
                "red"
            )
        )	
        if not os.path.isfile(self.Input):
            raise Exception(
                colored("%s is not exist!!"%(self.Input),"green")
            )		
        blast_flow = Ghostz(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)

        self.addTask("COG",
                     "nohup "+scripts_path+'/COG_mapping.py -i %(result)s -o %(result)s.cog -c %(cog)s'%(
                         {"result":self.Output,
                          "cog":self.COG
                          }
                         ),
                     dependencies="Blast"

                     )

        self.addTask(
            "Database",
            "nohup "+scripts_path+'/COG_Database.py %s  %s.cog '%(
                self.Total_Database,
                self.Output
                ),
            dependencies=["Blast","COG"]
        )         
                   


class GO_Mapping(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value):
        self.Input = Input
        self.Output = Output
        self.Database = Database
        self.E_value = E_value
        self.Total_Database = os.path.split( self.Input)[0]+"/../../total.db"


    def workflow(self):
        print(
            colored(
                "%s's GO Result is Running"%(self.Input),
                "red"
            )
        )		
        if not os.path.isfile(self.Input):
            raise Exception(
                colored("%s is not exist!!"%(self.Input),"green")
            )	


        blast_flow = Blast(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)	
        self.addTask("GO",
                     "nohup "+scripts_path+'/GO_Mapping.py  %(result)s.top1  %(result)s'%(
                         {"result":self.Output}
                         ),
                     dependencies="Blast"

                     )


        self.addTask(
            "Fetch",
            "nohup "+scripts_path+'/get_GO.py  %(result)s.GO-mapping.detail  %(result)s.annotaion_detail'%(
                {"result":self.Output}
                ), 
            dependencies=["Blast","GO"]

        )     

        self.addTask(
            "Database",
            "nohup "+scripts_path+'/GO_Database.py  %s  %s.annotaion_detail'%(
                self.Total_Database,
                self.Output
                ), 
            dependencies=["Blast","GO","Fetch"]

        )     
        self.addTask(
                    "Swissprot",
                    "nohup "+scripts_path+'/Swiss_Database.py  %s  %s.top1'%(
                        self.Total_Database,
                        self.Output
                        ), 
                    dependencies=["Blast","GO","Fetch"]
        
                )          

        self.addTask(
            "Detail",
            "nohup "+scripts_path+'/Go_list.py  %(result)s.GO-mapping.list  %(result)s.class'%(
                {"result":self.Output}
                ), 
            dependencies=["Blast","GO"]

        ) 



        self.addTask(
            "Stats",
            "nohup " +scripts_path+"/GO_stat.py  %(result)s.GO-mapping.list %(result)s.stat"%(
                {
                    "result":self.Output
                }
            )
            ,dependencies=["Blast","GO"]

        )

        self.addTask(
            "Draw",
            "nohup "+scripts_path+'/GO_draw.py  %(result)s.class %(path)s/stats %(path)s/Draw.R'%(
                {"result":self.Output,
                 "path":os.path.dirname(self.Output)
                 }
                ),
            dependencies=["Blast","GO","Detail"]
        )           

class Pathway_Mapping(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value,Total_Database):
        self.Input = Input
        self.Output = Output
        self.Database = Database
        self.E_value = E_value
        self.Total_Database = Total_Database

    def workflow(self):
        print(
            colored(
                "%s's KEGG Pathway Result is Running"%(self.Input),
                "red"
            )
        )
        if not os.path.isfile(self.Input):
            raise Exception(
                colored("%s is not exist!!"%(self.Input),"green")
            )		
        name = os.path.split(self.Input)[-1].rsplit('.',1)[0]
        blast_flow = Ghostz(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)	
        time_tag = int(time.time())

        self.addTask("To_sql",
                     "nohup "+config_hash["Utils"]["gapmap"]+'/blast_sql.py -f %(result)s   -r  %(result)s   -1 forward -2 forward  -n %(name)s_for -N %(name)s_rev -p %(pep)s -d %(dna)s -x %(tag)s -q'%(
                         {
                             "pep":self.Input,
                             "dna":self.Input,
                             "result":self.Output,
                             "name":name,
                             "tag":time_tag
                         }
                         ),
                     dependencies="Blast"

                     )



        self.addTask(
            "Build",
            config_hash["Utils"]["gapmap"]+"/Show_all_Mapping.py -o %s  -d %s"%(
                    os.path.split(self.Output)[0]+"/Gene",
                    time_tag,
                    ),
            dependencies=["Blast","To_sql"]
        )
          
        self.addTask(
            "Database",
            scripts_path+"/KEGG_Database.py "+self.Total_Database+" "+self.Output+" "+os.path.split(self.Output)[0]+"/Gene_detail.tsv",

            dependencies=["Blast","To_sql","Build"]
        )		

        






class Annotation_Run(WorkflowRunner):
    def __init__(self,Contig_list,OUTPUT):
        self.Contig_list = Contig_list
        self.Output = os.path.abspath(OUTPUT)
        Get_Path(OUTPUT)
    def workflow(self):
        dependcy = []
        annotation_path = self.Output+"/Annotation/"
        splited_path = self.Output+"/Assembly_END/"
        prediction_path  =  self.Output+"/Prediction/"
        protein_sequence_list = []


        # Gene Prediction
        for each_contig in self.Contig_list:
            prefix = re.search("^(\w+\d+)\.",os.path.split(each_contig)[-1]).group(1)
            category = re.search("^(\w+)\d+\.",os.path.split(each_contig)[-1]).group(1)
            genius = config_hash["Taxon"]["genius"]
            spieces = config_hash["Taxon"]["spieces"]
            strain = config_hash["Taxon"]["strain"]
            center = config_hash["Taxon"]["center"]

            each_prediction_path = prediction_path+'/%s/'%(prefix)
            if category =="Plasmid":
                plasmid = prefix
            else:
                plasmid=''
            self.addWorkflowTask(
                "%s_prediction"%(prefix),
                Gene_Prediction(
                    each_contig,
                    genius,
                    spieces, 
                    strain, 
                    center, 
                    prefix, 
                    each_prediction_path, 
                    plasmid,
                    config_hash["Threshold"]["e_value"]
                    ),
            )
            dependcy.append(
                "%s_prediction"%(prefix)
            )
            protein_sequence_list.append(
                each_prediction_path+'/%s.faa'%(prefix)
            )	

        # COG,Pathway,GO,Nr Annotation
        for each_protein in protein_sequence_list:

            each_dependcy = dependcy
            each_name = os.path.split(each_protein)[-1].rsplit('.',1)[0]
            self.addWorkflowTask(
                "GO%s"%(each_name),
                GO_Mapping(each_protein, 
                           annotation_path+'/%s/GO/%s'%(each_name,each_name),
                           config_hash["Database"]["swiss"],
                           config_hash["Threshold"]["e_value"]
            
                           ),
                dependencies= dependcy
            )			
            each_dependcy.append("GO%s"%(each_name))
            
            
            
            self.addWorkflowTask(
                "COG%s"%(each_name),
                COG_Mapping(each_protein, 
                            annotation_path+'/%s/COG/%s'%(each_name,each_name),
                            config_hash["Database"]["eggnog"],
                            config_hash["Threshold"]["e_value"]

                            ),
                dependencies= dependcy
            )			
            each_dependcy.append("COG%s"%(each_name))            
            self.addWorkflowTask(
                "Pathway%s"%(each_name),
                Pathway_Mapping(
                    each_protein, 
                    annotation_path+'/%s/Pathway/%s'%(each_name,each_name),
                    config_hash["Database"]["kegg"],
                    config_hash["Threshold"]["e_value"]
                    ),
                dependencies= dependcy
            )	
            each_dependcy.append("Pathway%s"%(each_name))            
            self.addWorkflowTask(
                "Nr%s"%(each_name),
                Nr_Mapping(
                    each_protein, 
                    annotation_path+'/%s/nr/%s'%(each_name,each_name)
                    ),
                dependencies= dependcy
            )

            each_dependcy.append("Nr%s"%(each_name))

            




if __name__ == '__main__':
    (options, args) = parser.parse_args()
    Sequence = options.Sequence
    OUTPUT   = options.Output
    Config   = options.Config
    os.environ["PATH"] = os.getenv("PATH")+'; '+scripts_path
    if not os.path.isfile(Config):
        raise Exception("File %s is not exist!!"%(Config))
    Get_Addtional_Config( Config )
    Config_Parse(general_config)

    data_prepare_flow = Data_prapare(Sequence,OUTPUT)

    error = data_prepare_flow.run()
    Contig_list = data_prepare_flow.get_contigs()

    annotation_flow = Annotation_Run(Contig_list, OUTPUT)
    error = annotation_flow.run()
    cobine_flow = TotalAnno_Run(OUTPUT)
    error = cobine_flow.run()
    os.system("rm rm Rplots*.pdf")
    os.system("rm cache")
    os.system("rm out.delta")
    os.system("rm head.fasta")
