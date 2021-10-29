#coding=utf-8
import csv

def Wt_csv(path,f):
    with open(path,"a") as w:
        writer=csv.writer(w)
        writer.writerow(f)


#old_path=r"/Users/gaotiansong/Desktop/变体处理/SI23Z8AW_20211029_001.csv"
old_path=input("输入要处理的文件:")
old_path=old_path.strip()
old_path=old_path.replace(r'"','')
new_path=old_path.split(r".")
new_path=new_path[0]+r"New.csv"
#mvar=2 #变体个数
mvar=input("变体个数:")
mvar=int(mvar)

m1var=1 #祖合变体个数

with open(old_path,"r") as f:
    rows=csv.reader(f)
    n=0
    parent_sku=""
    for row in rows:
        if  row[6]!="EAN":
            Wt_csv(new_path,row)
            continue
        if row[5]=="" and n==0:
            parent_sku=row[1]
            print(row[1])
            Wt_csv(new_path,row)
        if row[5]!="":
            row[23]=parent_sku
            print(row[1],row[23])
            Wt_csv(new_path,row)
            n=n+1
            if n==mvar:
                for i in range(m1var):
                    row[1]=row[1]+"01"
                    row[5]="需要EAN"
                    Wt_csv(new_path,row)
                n=0
                parent_sku=""
