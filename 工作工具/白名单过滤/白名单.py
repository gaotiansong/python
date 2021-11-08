#coding=utf-8
import pymysql
import re
from openpyxl import load_workbook


def find_cursor():
    # 打开数据库连接
    db = pymysql.connect(host='',
                        user='',
                        password='',
                        database='')

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
    except Exception as e:
        print(e)
        db.rollback()
    results = cursor.fetchall()
    db.close()
    for row in results:
        datas.append(row[1])
    datas=list(set(datas))
    return datas


def write_to_excel(path,data,newsheet):
    #实例化一个workbook对象
    workbook = load_workbook(path)
 
    #创建一个标签
    workbook.create_sheet(newsheet)
    #激活一个sheet
    sheet = workbook[newsheet]

    #开始遍历数组
    for row_index, row_item in enumerate(data):
        for col_index, col_item in enumerate(row_item):
            # 写入
            sheet.cell(row=row_index+1,column= col_index+1,value=col_item)

    workbook.save(path)
    print('处理完毕')


if __name__=="__main__":

    #okkeywords=["church","Collection","Church"]
    tablename="okword"
    okkeywords=find_datas(tablename)

    #要处理的文件
    #f_path=r"/Users/gaotiansong/Desktop/6187b3360cf24ef0eebbd7ad.xlsx"
    f_path=input("拉入你要进行白名单处理的表格:")
    f_path=re.sub(r'"',"",f_path)
    f_path=f_path.strip()

    wb = load_workbook(f_path)
    #选择标签
    mysheet=wb["Template"]
    new_data=[]
    for r in range(mysheet.max_row):
        row=[]
        for c in range(mysheet.max_column):
            row1=mysheet.cell(r+1,c+1).value
            row.append(row1)
        #获取包含包含违禁词的字符串p_word
        p_word=row[-1]
        mo=re.compile("\[.*?\]")
        #提取其中的违禁词
        ss=re.findall(mo,str(p_word))
        row_s=[]
        for s in ss:
            s=s[1:-1]
            for s1 in s.split(","):
                #判断s1是否在白名单中，在则跳过，不在则标记为违禁词
                if s1 not in okkeywords:
                    row_s.append(s1)
        rowss="|".join(list(set(row_s)))
        new_data.append(row+[rowss])

    #新标签名
    newsheet="New_Template"
    write_to_excel(f_path,new_data,newsheet)
