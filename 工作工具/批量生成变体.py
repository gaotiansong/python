#coding=utf-8
import csv
def wt_q(asins,ena_path):
    #给对列写入ean
    with open(ena_path,"r") as f:
        rows=f.readlines()
        for row in rows:
            asins.append(str(row.strip()))

def Wt_csv(path,f):
    with open(path,"a",newline="") as w:
        writer=csv.writer(w)
        writer.writerow(f)

def pro_uk(old_path,mvar,m1var,asins):
    new_path=old_path.split(r".")
    new_path=new_path[0]+r"New.csv"
    with open(old_path,"r") as f:
        rows=csv.reader(f)
        n=0
        parent_sku=""
        for row in rows:
            if  "EAN" not in row:
                Wt_csv(new_path,row)
                continue
            #判断是不是母体
            if "Parent" in row and n==0:
                parent_sku=row[1]
                print(row[1])
                Wt_csv(new_path,row)
            #判断是不是变量
            if "Child" in row and "Variation" in row:
                row[25]=parent_sku
                print(row[1],row[25])
                Wt_csv(new_path,row)
                n=n+1
                if n==mvar:
                    for i in range(m1var):
                        row[1]=row[1]+"01"
                        row[4]=asins.pop()
                        row[12]="组合价格"
                        Wt_csv(new_path,row)
                    n=0
                    parent_sku=""

def pro_us(old_path,mvar,m1var,asins):
    new_path=old_path.split(r".")
    new_path=new_path[0]+r"New.csv"
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
                        row[5]=asins.pop()
                        row[10]="组合价格"
                        Wt_csv(new_path,row)
                    n=0
                    parent_sku=""

if __name__=="__main__":
    old_path=input("输入要处理的文件:")
    old_path=old_path.strip()
    old_path=old_path.replace(r'"','')

    asins=[]
    ena_path=input("输入ean文件:")
    ena_path=ena_path.strip()
    ena_path=ena_path.replace(r'"','')
    wt_q(asins,ena_path)
    asins=asins[::-1]
    mvar=input("变体个数:")
    mvar=int(mvar)
    m1var=1 #祖合变体个数
    #判断是美国还是英国 然后调用相应的函数
    with open(old_path,"r") as f:
        rows=csv.reader(f)
        n=0
        cou=""
        for row in rows:
            if n==3:
                cou=row[0]
                break
            n=n+1
    if cou=="stringlight":
        print("英国")
        pro_uk(old_path,mvar,m1var,asins)
    elif cou=="hangingornament":
        print("美国")
        pro_us(old_path,mvar,m1var,asins)
    
    asin_new=[]
    for i in asins:
        asin_new.append([i])
    new_ean=ena_path.split(r".")
    new_ean=new_ean[0]+r"剩余.txt"
    with open(new_ean,"w",encoding="utf-8",newline="") as f:
        writer=csv.writer(f)
        writer.writerows(asin_new)
