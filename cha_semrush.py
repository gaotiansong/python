from selenium import webdriver
import datetime
import time,bs4

def login(doname,driver):
    url='https://zh.semrush.com/analytics/organic/positions/?searchType=domain&q='+doname+'&date=20200206'
    driver.get(url)
    time.sleep(30)
    html=driver.page_source
    bs=bs4.BeautifulSoup(html,'html.parser') 
    #driver.close()
    num=bs.select('div .cl-summary__value span')
    try:
        num=num[0].getText()
    except:
        try:
            nums=bs.select('div .cl-nothing-found__other-databases__database span')
            s=''
            for num in nums:
                s1=num.getText()
                s=s+s1
            if s=='':
                s='其它数据库也没有'
            else:
                s=s
            num='0,'+s
        except:
            num='0,找不到相关数据'
            print(num)

    with open('/Users/gaotiansong/Desktop/域名列表/donames_jieguo.txt','a') as f:
        f.write(doname+','+num+'\n')
        f.close()

#doname='customadd.com'
driver=webdriver.Chrome(executable_path='/Users/gaotiansong/Downloads/chromedriver')
doname_path='/Users/gaotiansong/Desktop/域名列表/donames.txt'
with open(doname_path, 'r', encoding='utf-8') as f:
    for line in f:
        doname=line[:-1] #去掉换行符
        login(doname,driver)
    print('查询完毕，关闭所有窗口')  
    driver.quit()
