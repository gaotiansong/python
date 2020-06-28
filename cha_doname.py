from selenium import webdriver
import time,bs4,os,re
'''
该代码已经能够顺利批量查询谷歌收录量。但有时候还是会导致失败，重新手动重链后才可继续运行。
最后更新于2020年2月16日
'''
def cha_google(url):
    siteurl='site:'+url
    #browser = webdriver.Chrome()
    #browser = webdriver.Chrome(executable_path='/Users/gaotiansong/Downloads/chromedriver') #驱动器路径
    browser=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe') #驱动器路径
    #browser.maximize_window()   #设置浏览器大小：全屏
    #browser.minimize_window()
    browser.get('http://www.google.com')  
    browser.set_page_load_timeout(10)
    #定位输入框
    input_box = browser.find_element_by_name('q')
    try:
        #输入内容：siteurl
        input_box.send_keys(siteurl)
        #print('搜索关键词：selenium')
    except Exception as e:
        print('搜索关键词异常')
    #输出内容：搜索关键词
    try:
        input_box.submit()
        #print('成功回车')
    except Exception as e:
        print('回车异常')
    html=browser.page_source
    browser.get_cookies()
    browser.quit()
    bs=bs4.BeautifulSoup(html,'html.parser')
    html=bs.select('div .appbar')
    if html==[]:
        print('触发了验证，切换ip重新查询')
        time.sleep(60)
        reconnect_ADSL()#重连ADSL
        cha_google(url)
    else:
        pass
    s=''
    for h in html:
        h=h.getText()
        s=s+h
    s=re.sub(',','',s)
    pattern = re.compile(r'[0-9]+') 
    result1 = pattern.findall(s)
    try:
        n=result1[0]
    except:
        n=''
        print('查询失败')
    n=re.sub('\n| ','',n)
    n=url+','+n
    return n

from datetime import datetime
# 连接ADSL
def connect_ADSL(name,username,password):
    cmd_string = f'rasdial {name} {username} {password}'
    os.system(cmd_string)
    time.sleep(5)

# 断开ADSL
def disconnect_ADSL(name):
    cmd_string = f'rasdial {name} /disconnect'
    os.system(cmd_string)
    time.sleep(5)

# 重连ADSL
def reconnect_ADSL():
    name='宽带连接'
    username='12136010'
    password='600332'
    disconnect_ADSL(name)
    connect_ADSL(name, username, password)


def xieru_txt(s,path_new):
    s=s+'\n'
    with open(path_new,'a') as f:
        f.write(s)

def panduan(key,key_path1):
    f1=open(key_path1,'a')
    f1.write(key+'\n')
    with open(key_path1) as f:
        txt=f.read()
        f.close()
        if key in txt:
            return True
        else:
            return False
#主程序开始
#重新链接ads，获取新的ip
reconnect_ADSL()#重连ADSL
#os.system(r'start C:\Users\Administrator\Desktop\清除缓存.bat')
#设置域名列表
doname=r'D:\sitegoogle\domains_2020-04-26_12_47_36.txt'
#设置结果保存位置
path_new=r'D:\sitegoogle\ok.txt'
path_data=r'D:\sitegoogle\db.txt'
n=1
for line in open(doname):
    url=line
    url=re.sub('\n','',url)
    if panduan(url,path_data)==True:#如果关键词已经采集过，则跳过
        print(url,'已经存在，跳过')
        continue
    else:
        pass

    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),':开始采集第',n,'条')
    if n%5==0:
        reconnect_ADSL()#重连ADSLs
    else:
        pass
    try:
        time.sleep(1)
        s=cha_google(url)
        time.sleep(1)
        xieru_txt(s,path_new)
        n=n+1
    except:
        reconnect_ADSL()#重连ADSLs
    print('')
print('采集完毕')
