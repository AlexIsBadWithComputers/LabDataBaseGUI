TechT = ['TENNANT','MILLER','MAYER','WIESER','LORD-MAY',"BISHOP","LAU","CHAN","MABIOR"]
ElementT = ['Mo','Cu','B','U','Fe','Zn','Sr','S']
ContractT= ['RESEARCH','AGAT','GRASBY','SPENCER','MIRNA','MONCUR',"LORENZ","OMID"]
TypeT =['SAMPLE','STANDARD','BLANK']
SpikeT = ['NONE','SINGLE','DOUBLE','E_DOPING']
Machine = ["NEPTUNE","TRITION"]

Tech = sorted(TechT)
Element = sorted(ElementT)
Contract = sorted(ContractT)
Type = sorted(TypeT)
Spike = sorted(SpikeT)



#To make sure these options are always last
Tech = Tech + ["UNKNOWN"]
Contract = Contract +["UNKNOWN"]


