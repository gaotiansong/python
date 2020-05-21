from selenium import webdriver
import time,bs4,os,re,csv
'''
改代码用于抓取主关键词的扩展关键词，主关键词搭配相关关键词可有效提高内容的相关性。
'''
def cha_google(keyword):
    siteurl=keyword
    browser=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe') #驱动器路径
    #browser.maximize_window()   #设置浏览器大小：全屏
    browser.get('https://cn.bing.com/?FORM=BEHPTB&ensearch=1')  
    browser.set_page_load_timeout(10)
    #定位输入框
    input_box = browser.find_element_by_name('q')
    try:
        #输入内容：siteurl
        input_box.send_keys(siteurl)
    except Exception as e:
        print('搜索关键词异常',e)
    
    #输出内容：搜索关键词
    try:
        input_box.submit()
        time.sleep(0.5)
    except Exception as e:
        print('回车异常',e)
    time.sleep(1)
    html=browser.page_source
    browser.get_cookies()
    browser.quit()
    bs=bs4.BeautifulSoup(html,'html.parser')
    try:
        keywords=bs.select('ul.b_vList.b_divsec li')
    except Exception as e:
        print(e)
        return 0,''
    try:
        keywords=keywords[:8]
    except Exception as e:
        print(e)
        keywords=keywords
    words=[]
    for i in keywords:
        keyword=i.getText()
        words.append(keyword)
    n=len(words)
    words=','.join(words)
    return n,words


def write_csv(s,path_new):
    with open(path_new,'a',newline='') as f:
        writer=csv.writer(f)
        if os.path.getsize(path_new)==0:
            writer.writerow(['主关键词','数量','扩展关键词'])
            writer.writerow(s)
        else:
            writer.writerow(s)


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




def index(key,path_new):
    n,keys=cha_google(key)
    s=[key,n,keys]
    write_csv(s,path_new)

#主程序开始

keyPath=r'D:\Backup\桌面\test\testkey.csv'
path_new=r'D:\Backup\桌面\test\test1.csv'
with open(keyPath,'r') as f:
    read_f=csv.reader(f)
    for i in read_f:
        if '关键词' in i[0]:
            continue
        else:
            key=i[0]
            index(key,path_new)
