#-*-coding:utf-8 -*-
from selenium import webdriver
import datetime
import time,bs4

def login(doname,db,driver,n):
    url='https://zh.semrush.com/analytics/organic/overview/?db='+db+'&searchType=domain&q='+doname
    driver.get(url)
    if n==0:
        time.sleep(15)
    else:
        time.sleep(0)
    driver.implicitly_wait(30)
    time.sleep(5)
    html=driver.page_source
    bs=bs4.BeautifulSoup(html,'html.parser') 
    #driver.close()
    num=bs.select('div .cl-summary__value span')
    try:
        num=num[0].getText()
        num=','+db+','+num
    except:
        num=','+db+','+'0'
    return num

def find_f(doname,db,driver):
    url='https://zh.semrush.com/analytics/overview/?q=nbamr.com&db='+db+'&searchType='+doname
    driver.get(url)
    driver.implicitly_wait(30)
    html=driver.page_source
    bs=bs4.BeautifulSoup(html,'html.parser') 
    flow=bs.select('span._link__text_1yhuh_44')
    try:
        flow=flow[1].getText()
    except Exception as e:
        print(e)
        flow=0
    return flow

def find_key(doname):
    url='https://zh.semrush.com/analytics/organic/positions/?searchType=domain&q='+doname
    driver.get(url)
    time.sleep(5)
    driver.implicitly_wait(30)
    time.sleep(5)
    html=driver.page_source
    bs=bs4.BeautifulSoup(html,'html.parser') 
    keyls=bs.select('span.cl-display-keyword')
    try:
        sl=[]
        for key in keyls:
            key=key.getText()
            sl.append(key)
        s='|'.join(sl)
    except:
        s='查询出错'
    return s

#driver=webdriver.Chrome(executable_path=r'/Users/gaotiansong/Downloads/chromedriver')
driver=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
#设置域名列表
doname_path=r'D:/Backup/桌面/seoshuju/alldoname.txt'

#设置结果保存位置
jieguo_path=r'D:/Backup/桌面/seoshuju/jieguo_alldoname0531.txt'

with open(doname_path, 'r', encoding='utf-8') as f:
    global n
    n=0
    for line in f:
        nums=''
        doname=line[:-1] #去掉换行符
        for db in ['us','ca','au','uk']:
            if db=='us':
                flow=find_f(doname,db,driver)
            num=login(doname,db,driver,n)
            n=1
            nums=nums+num
        shuju=nums+','+flow
        
        keys=find_key(doname)

        with open(jieguo_path,'a') as f:
            try:
                f.write(doname+','+keys+','+shuju+'\n')
                f.close()
            except:
                print('跳过')
        print(doname,':',shuju)
    print('查询完毕，关闭所有窗口')  
    driver.quit()
