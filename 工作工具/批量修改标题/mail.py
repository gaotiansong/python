#coding=utf-8
import csv
from os import rmdir
from random import sample
import re
pro_tath=input("输入你要处理的文件:")
pro_tath=pro_tath.strip()
key_path=r"./keyword/keyword.csv"
add1_path=r"./keyword/add1.csv"
add2_path=r"./keyword/add2.csv"
zt_path=r"./keyword/zt.csv"
ch_path=r"./keyword/ch.csv"

with open(key_path,"r") as key,open(add1_path,"r") as f1,open(add2_path,"r")as f2,open(zt_path,"r")as zt,open(ch_path,"r")as ch,open(pro_tath,"r") as pro:
    pros=csv.reader(pro)

    #随机获取附加词1
    add1s=csv.reader(f1)
    lsadd1=[]
    for i1 in add1s:
        lsadd1.append(i1)
    add1=sample(lsadd1,1)[0]
    print(add1)

    #随机获取附加词2
    lsadd2=[]
    add2s=csv.reader(f2)
    for i2 in add2s:
        lsadd2.append(i2)
    add2=sample(lsadd2,1)[0]
    #随机获取主题词
    lszt=[]
    zts=csv.reader(zt)
    for i1 in zts:
        lszt.append(i1)
    zt1=sample(lszt,1)[0]
    #随机获取场合词
    lsch=[]
    chs=csv.reader(ch)
    for i1 in chs:
        lsch.append(i1)
    ch1=sample(lsch,1)[0]
    #随机获取关键词
    rows=csv.reader(key)
    keywords=[]
    for i in rows:
        keywords.append(i[0])

    for p in pros:
        if p[0]=="Seller SKU" or p[0]=="item_sku":
            continue
        print("p1",p[1])
        ls=[]
        title=""
        while True:
            ls1=ls
            s1=" ".join(ls1)
            ls.append(sample(keywords,1)[0])
            lss=[p[1]]+["Christmas ornaments"]+ls+add1+add2+zt1+["For"]+ch1
            s=" ".join(lss)
            ns=[80,120,140,160,180]
            if len(s)>sample(ns,1)[0] and len(s)<200:
                print("s")
                title=s
                break
            elif len(s)>200:
                print("s1")
                if len(s1)<80:
                    continue
                title=s1
                break
        print(len(title),title.title())
        newpro_path=pro_tath.split(r".")
        newpro_path=newpro_path[0]+r"New.csv"
        h1=title.title().strip()
        h1=re.sub("(\s)+"," ",h1)
        with open(newpro_path,"a",newline="") as w:
            writer=csv.writer(w)
            writer.writerow([p[0],p[1],h1])
