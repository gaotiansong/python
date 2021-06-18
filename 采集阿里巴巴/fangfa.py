def find_bs(url,driver_path,n_y):
    import bs4,time
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    opt = webdriver.ChromeOptions()
    #opt.add_argument("--headless") #新版本设置无头
    opt.add_argument("--disable-gpu")
    opt.add_argument('lang=en-us.UTF-8')
    driver = webdriver.Chrome(executable_path=driver_path,options=opt) #驱动器路径
    m=0
    try:
        driver.get(url)
        #driver.refresh()#刷新当前页面
        driver.set_page_load_timeout(30)
        if n_y=='y':
            a=0 #下拉鼠标次数
            while a<3:
                print('下拉鼠标',a+1,'次')
                time.sleep(0)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(3)
                a=a+1
                continue
        else:
            pass
        html=driver.page_source
        driver.get_cookies()
        driver.quit()
    except:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'链接失败,重试',m,'次')
        html=''
        print('抓取hmtl失败，重新拨号,重新链接抓取')
        driver.get_cookies()
        driver.quit()
        #reconnect_ADSL()#重连ADSL
        if m<2:
            m=m+1
            find_bs(url,driver_path,n_y)
        else:
            pass

    bs=bs4.BeautifulSoup(html,'html.parser')
    return bs

def find_bspro(url):
    import time,bs4,requests
    url=url
    n=0
    while n<3:
        try:
            req=requests.get(url,timeout=20)
            req.raise_for_status()
            #print('请求',url,'状态',req.status_code)
            html=req.text
        except:
            print('链接失败,重试',n,'次')
            n=n+1
            html=''
            time.sleep(3)
        bs=bs4.BeautifulSoup(html,'html.parser')
        return bs

def find_urls(bs):
    pro_url=[]
    urlls=bs.select('.organic-gallery-title')
    for url in urlls:
        link=url.get('href')
        pro_url.append(link)
    return pro_url

def to_txt(ls,patch_txt):
    with open(patch_txt,'a') as f:
        f.write(ls)
        f.close

def panduan(key,key_path1):
    #f1=open(key_path1,'a')
    #f1.write()
    with open(key_path1) as f:
        txt=f.read()
        f.close()
        if key in txt:
            return True
        else:
            return False

'''采集页面内容即产品内容'''
def find_h1(bs):
    try:
        h1s=bs.select('h1')
        h1=h1s[0].getText()
    except:
        print('没找到商品标题')
        h1=''
    return h1

def find_price(bs):
    import re
    #寻找价格所在板块
    try:
        prs=bs.select('div .ma-main')
        html=prs[0].getText()
        #使用正则获取价格
        moprice=re.compile(r'($[0-9]*.[0-9]{2}){1}')
        pr=moprice.findall(html)
        pr=pr[0]
    except:
        print('获取价格失败')
        pr='0'

    return pr

#查找产品描述
def find_de(bs):
    import re
    de=bs.select('.do-entry.do-entry-separate span')#class的子class
    va=bs.select('.do-entry.do-entry-separate dd')
    i=0
    s=''
    for d in de:
        v1=va[i].get_text()
        v1=re.sub(' |\n','',v1)+'\n'
        i=i+1
        s=s+(d.get_text()+v1)
    return s

#查找产品图片
def find_imgs(bs):
    import re
    html=bs.select('ul.inav.util-clearfix a img')
    imgs=[]
    for img in html:
        img=img.get('src')
        if '50x50' in img:
            pass
        else:
            continue
        img=re.sub('_50x50.jpg','',img)
        img='https:'+img
        imgs.append(img)
    imgs=set(imgs)
    imgs=list(imgs)
    imgs=','.join(imgs)
    return imgs

def wt_csv(file,patch_csv):
    import csv,os
    fileHeader=['标题','价格','描述','分类','标签','图片地址'] #设置表单每列标题
    csvFile=open(patch_csv,'a',newline='')
    n=os.path.getsize(patch_csv)
    writer=csv.writer(csvFile)
    if n==0:
        writer.writerow(fileHeader)
        writer.writerow(file)
    else:
        writer.writerow(file)
        csvFile.close()  
