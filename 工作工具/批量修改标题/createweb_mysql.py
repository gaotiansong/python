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

if __name__=="__main__":
    #获取各种关键词
    print("加载在线数据中")
    keywords=find_datas(tablename="keyword")
    print("成功加载keywords")
    add1s=find_datas(tablename="add1")
    print("成功加载add1")

    add2s=find_datas(tablename="add2")
    print("成功加载add2")

    zt1s=find_datas(tablename="zt")
    print("成功加载zt1s")

    ch1s=find_datas(tablename="ch")
    print("成功加载ch1s")

    pro_tath=input("输入你要处理的文件:")
    pro_tath=pro_tath.strip()

    pro_key=input("输入个性化关键词列表文件地址(可直接回车跳过)：")
    pro_key=pro_key.strip()
    custom_keys=[]
    if pro_key!="":
        custom_keys=find_custom_keys(pro_key)
    else:
        custom_keys=[""]


    #生成新文件路径和名称
    newpro_path=pro_tath.split(r".")
    newpro_path=newpro_path[0]+r"New.csv"

    #替换成新文件
    _=open(newpro_path,"w")

    custom1=input("固定关键词1，出现在标题最前面，可直接回车跳过：")
    custom2=input("固定关键词2，出现在素材标签后，可直接回车跳过：")
    custom3=input("固定关键词3，出现在“For”前面，可直接回车跳过：")


    with open(pro_tath,"r") as f:
        pros=csv.reader(f)
        for p in pros:
            if p[0]=="Seller SKU" or p[0]=="item_sku":
                continue
            #print("p1",p[1])
            title=""

            add1=sample(add1s,1)[0]
            add2=sample(add2s,1)[0]
            zt1=sample(zt1s,1)[0]
            ch1=sample(ch1s,1)[0]

            ns=[140,160,180]
            size_title=sample(ns,1)[0]

            custom_key=sample(custom_keys,1)[0]

            n=0
            ls=[]
            s1=""
            while True:
                n=n+1
                ls.append(sample(keywords,1)[0])
                #拼凑的标题
                lss=[custom1]+[p[1]]+[custom2]+[custom_key]+ls+[add1]+[add2]+[zt1]+[custom3]+["For"]+[ch1]
                s=" ".join(lss)
                s=s.strip()

                s=s.title().strip()
                s=re.sub("(\s)+"," ",s)

                #print(n,size_title,len(s),"ls=",ls)

                if size_title <  len(s) < 195:
                    title=s
                    break
                elif len(s)>195:
                    #大于200不能用
                    #print("标题太长")
                    #s1只有两种情况，太短和可以
                    if len(s1)<100:
                        #print("s1太短")
                        s1=s
                        continue
                    else:
                        #print("使用s1=",s1,"\n\n")
                        title=s1
                        break
                else:
                    #标题太短则再让ls增加一个关键词
                    s1=s
                    continue

            #整理成型标题
            h1=title
            print("最终标题",len(h1),"--",title)

            #生成关键词
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
                #拼凑的标题写入文件
                writer.writerow([p[0],p[1],h1,keys])
