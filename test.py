import json

f=open("jsondata.txt",'r+')
pdf=json.load(f)

tmp_dic={}
tmp_dic["# QUESTION:"]='Bla'
tmp_dic['Options']='Ola'

pdf["SECTION-1"][len(pdf["SECTION-1"])-1]=tmp_dic
tmp_dic={}
tmp_dic["# QUESTION:"]=''
tmp_dic['Options']=''
pdf["SECTION-1"].append(tmp_dic)
print(pdf["SECTION-1"][len(pdf["SECTION-1"])-1])
