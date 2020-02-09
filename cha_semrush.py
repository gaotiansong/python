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

driver=webdriver.Chrome(executable_path=r'/Users/gaotiansong/Downloads/chromedriver')
doname_path=r'/Users/gaotiansong/Desktop/域名列表/shopify.txt'
with open(doname_path, 'r', encoding='utf-8') as f:
    global n
    n=0
    for line in f:
        nums=''
        doname=line[:-1] #去掉换行符
        for db in ['us','ca','au','uk']:
            num=login(doname,db,driver,n)
            n=1
            nums=nums+num
        shuju=nums
        
        with open(r'/Users/gaotiansong/Desktop/域名列表/shopify_jieguo.txt','a') as f:
            f.write(doname+','+shuju+'\n')
            f.close()
        print(shuju)
    print('查询完毕，关闭所有窗口')  
    driver.quit()
