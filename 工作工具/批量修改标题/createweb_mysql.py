#coding=utf-8
import pymysql
import csv
import re
from random import sample

def find_cursor():
    # 打开数据库连接
    db = pymysql.connect(host='',
                        user='',
                        password='',
                        database='keyword')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    return cursor,db

def find_datas(tablename):
    datas=[]
    cursor,db=find_cursor()
    sql="select * from {tablename};".format(tablename=tablename)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    results = cursor.fetchall()
    db.close()
    for row in results:
        datas.append(row[1])
    datas=list(set(datas))
    return datas

#获取各种关键词
keywords=find_datas(tablename="keyword")

add1s=find_datas(tablename="add1")
add1=sample(add1s,1)[0]


add2s=find_datas(tablename="add2")
add2=sample(add2s,1)[0]


zt1s=find_datas(tablename="zt")
zt1=sample(zt1s,1)[0]


ch1s=find_datas(tablename="ch")
ch1=sample(ch1s,1)[0]


pro_tath=input("输入你要处理的文件:")
pro_tath=pro_tath.strip()

custom=input("输入固定标题（可为空回车跳过）:")


with open(pro_tath,"r") as f:
    pros=csv.reader(f)
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
            lss=[p[1]]+["Christmas ornaments"]+ls+[add1]+[add2]+[zt1]+[custom]+["For"]+[ch1]
            s=" ".join(lss)
            ns=[140,160,180]
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

        while True:
            lstags=[]
            lstag=sample(keywords,5)
            lstags1=lstags
            lstags=lstags+lstag
            keys=",".join(list(set(lstags)))
            if len(keys)>200 and len(keys)<250:
                break
            elif len(keys)>250:
                keys=",".join(lstags1)

        with open(newpro_path,"a",newline="") as w:
            writer=csv.writer(w)
            writer.writerow([p[0],p[1],h1,keys])
