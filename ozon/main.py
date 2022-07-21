import csv
import time
import re
import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from lxml import etree
from bs4 import BeautifulSoup
import datetime

#构造没有参数的列表url
def getnewpags(s):
    ls=s.split("&")
    newls=[]
    for i in ls:
        if "page=" in i:
            newls.append(i)
            break
        else:
            newls.append(i)
    return "&".join(newls)

def get_cookie():
    with open("./c.txt") as f:
        s = f.read()
        ls_s = s.split(";")
        dic = {}
        for i in ls_s:
            dic[i.split("=")[0].strip()] = i.split("=")[1].strip()
        return dic

def find_ua():
    import random
    uas=[
        'User-Agent="Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"',
        'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"',
        'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"',
        'User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"',
        'User-Agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"',
        'User-Agent="Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"',
        'User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"',
        'User-Agent="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16"',
        'User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"',
        'User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"',
        'User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11"',
        'User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER"',
        'User-Agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)"',
        'User-Agent="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)"',
        'User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36"',
        'User-Agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"',
    ]
    return random.sample(uas,1)

def find_driver():
    prefs = {"profile.managed_default_content_settings.images": 2}  # 设置无图模式
    options = webdriver.ChromeOptions()
    options.page_load_strategy='eager'
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    options.add_experimental_option("prefs", prefs)  # 无图
    options.add_argument("--lang=ru_RU")
    #options.add_argument("--headless")  # 不显示界面
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('ignore-certificate-errors')

    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    ua=find_ua()[0]
    options.add_argument(ua)
    s = Service(r"./chromedriver")  # 驱动器位置
    driver = webdriver.Chrome(service=s, options=options)

    with open('./stealth.min.js') as f:
        source_js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": source_js
    })

    return driver

def find_html(timeout,url):
    print("开始请求==",url)
    driver = find_driver()
    cooks={'domain': 'www.ozon.ru', 'expiry': 1658044661, 'httpOnly': False, 'name': 'tmr_detect', 'path': '/', 'secure': False, 'value': '0%7C1657958261295'}, {'domain': '.ozon.ru', 'expiry': 1721030252, 'httpOnly': False, 'name': '_ga_JNVTMNXQ6F', 'path': '/', 'secure': False, 'value': 'GS1.1.1657958193.1.1.1657958252.1'}, {'domain': '.ozon.ru', 'expiry': 1657961851, 'httpOnly': False, 'name': '__exponea_time2__', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '0.23997735977172852'}, {'domain': '.ozon.ru', 'expiry': 1665734189, 'httpOnly': False, 'name': '_gcl_au', 'path': '/', 'secure': False, 'value': '1.1.828064798.1657958190'}, {'domain': '.ozon.ru', 'expiry': 1686729451, 'httpOnly': False, 'name': 'tmr_lvidTS', 'path': '/', 'secure': False, 'value': '1657958189273'}, {'domain': '.ozon.ru', 'expiry': 1686729451, 'httpOnly': False, 'name': 'tmr_lvid', 'path': '/', 'secure': False, 'value': 'efa32f61a1024d2672eb31a977b146f5'}, {'domain': 'www.ozon.ru', 'expiry': 1689494187, 'httpOnly': False, 'name': 'isBuyer', 'path': '/', 'secure': False, 'value': '0'}, {'domain': 'www.ozon.ru', 'httpOnly': False, 'name': 'xcid', 'path': '/', 'secure': False, 'value': '1d2ba24ac7ed330cb2965cb36fb791d5'}, {'domain': '.ozon.ru', 'expiry': 1752566253, 'httpOnly': False, 'name': '__exponea_etc__', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'c22fd0a2-44b6-4330-850b-3cd479d74c7c'}, {'domain': '.ozon.ru', 'expiry': 1689494177, 'httpOnly': True, 'name': '__Secure-refresh-token', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '3.0.g8QWLdgSQkCDNOcUK8WiuQ.81.l8cMBQAAAABi0m8gLYaMwaN3ZWKgAICQoA..20220716095616.Wx-xSzuK1mn3YK8w_kdbtQKNn0jKlBHDO1uug5TPtNI'}, {'domain': '.ozon.ru', 'expiry': 1689494177, 'httpOnly': True, 'name': '__Secure-user-id', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '0'}, {'domain': 'www.ozon.ru', 'httpOnly': False, 'name': 'AREA_ID', 'path': '/', 'secure': False, 'value': '2'}, {'domain': '.ozon.ru', 'expiry': 1689494177, 'httpOnly': True, 'name': '__Secure-ext_xcid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1d2ba24ac7ed330cb2965cb36fb791d5'}, {'domain': 'www.ozon.ru', 'expiry': 1973318187, 'httpOnly': False, 'name': 'cnt_of_orders', 'path': '/', 'secure': False, 'value': '0'}, {'domain': '.ozon.ru', 'expiry': 1658044587, 'httpOnly': False, 'name': 'rfuid', 'path': '/', 'secure': False, 'value': 'NjkyNDcyNDUyLDEyNC4wNDM0NDk2ODQ3NTE5OCwtMTg2ODU4MzI4NCwwLDE5OTc4MDM4NTIsLTE4MjA0MzIzMzMsMTg4NjY0MTM1NCxOYU4sMSwwLDMwLC0xMjIyMDQ0NDM2LDgsMjI3MTI2NTIwLDEsMSwwLC00OTEyNzU1MjMsLTY2NjQ5NCw5ODgzNTEzMDMsNjUsLTExODM0MTA3MiwxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LC0xNTYxNDgxNjcwLDUy'}, {'domain': '.ozon.ru', 'expiry': 1689494177, 'httpOnly': False, 'name': '__Secure-ab-group', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '81'}, {'domain': '.ozon.ru', 'expiry': 1657959985, 'httpOnly': True, 'name': '__cf_bm', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'JAoNqatqIvg5tXt22634UDS6huesY7IbNxw0iQYqVBc-1657958185-0-Af/Kj0pP5guGKXlT9rowuVxF3Pfyip/9BSRD0mp2weU5vvUPzsPSpw/7sfR+pzbcuIwlKfBunnXSGa4QF+x3tHf9G+/pYovM/RNdUI76PoyI/6O5LSCJCiIiIQMiwTXmD6indQ5kOgMZSbpswzGBFkjybNgxT7XqKtUJeJavcpo7'}, {'domain': 'www.ozon.ru', 'expiry': 1657961774, 'httpOnly': False, 'name': 'cf_chl_rc_m', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.ozon.ru', 'expiry': 1721030252, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.1.2006073728.1657958194'}, {'domain': 'www.ozon.ru', 'expiry': 1657961766, 'httpOnly': False, 'name': 'cf_chl_2', 'path': '/', 'secure': False, 'value': '9d67cb910e52941'}, {'domain': 'www.ozon.ru', 'expiry': 1657961767, 'httpOnly': False, 'name': 'cf_chl_prog', 'path': '/', 'secure': False, 'value': 'b'}, {'domain': '.ozon.ru', 'expiry': 1686729451, 'httpOnly': False, 'name': 'tmr_reqNum', 'path': '/', 'secure': False, 'value': '9'}, {'domain': '.ozon.ru', 'expiry': 1689494177, 'httpOnly': True, 'name': '__Secure-access-token', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '3.0.g8QWLdgSQkCDNOcUK8WiuQ.81.l8cMBQAAAABi0m8gLYaMwaN3ZWKgAICQoA..20220716095616.6iCUnt8RSXPOb3wH92mIZlO9Rm2psO9DCNhQILhFcE0'}
    #cooks=get_cookie()
    driver.set_page_load_timeout(10)
    width=500
    height=1000000
    driver.set_window_size(width, height)
    try:
        driver.get(url)
        for c in cooks:
            driver.add_cookie(c)
        print("开始刷新页面")
        time.sleep(2)
        driver.set_page_load_timeout(timeout)
        driver.refresh()
        # 定义一个初始值
        temp_height = 0
        seeptime=0
        if timeout>30:
            seeptime=2
        while True:
            # 循环将滚动条下拉
            driver.execute_script("window.scrollBy(0,1000)")
            # sleep一下让滚动条反应一下
            time.sleep(seeptime)
            # 获取当前滚动条距离顶部的距离
            check_height = driver.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # 如果两者相等说明到底了
            if check_height == temp_height:
                break
            temp_height = check_height

    except:
        print("超时",driver.get_cookies())
        driver.set_page_load_timeout(100)
    #driver.execute_script("window.stop()")
    html=driver.page_source
    driver.close()
    #time.sleep(120)
    driver.quit()
    return html

def find_next(list_url):
    print("执行find_next", list_url)
    html = find_html(timeout=31, url=list_url)
    tree=etree.HTML(html)

    # 获取下一页
    print("开始获取下一页")
    nextpage = tree.xpath('//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[5]/div[2]/div/div[1]/div[1]/a/@href')
    n=0
    while len(nextpage)<2:
        n=n+1
        nextpage = tree.xpath('//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[5]/div[2]/div/div[1]/div[2]/a/@href')
        if n>5:
            break
    print("成功获取下一页", nextpage)

    pags = []
    for purl in nextpage:
        try:
            if "page=" in purl and purl not in pags:
                pags.append("https://www.ozon.ru" + purl)
            else:
                pags.append("https://www.ozon.ru" + purl+"&page=1")
        except:
            continue

    items = tree.xpath('//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[5]/div[1]/div/div/div[*]')
    items_s = []
    item_datas = []
    for i in items:
        try:
            ht = etree.tostring(i, pretty_print=True, method='html').decode('utf-8')
            tr = etree.HTML(ht)
            if  r"Из-за рубежа" in tr.xpath('//b/font/text()')[0] and r"Бестселлер" in tr.xpath('//span/span/text()')[0]:

                #获取主图
                img = tr.xpath("//img/@src")
                try:
                    img = img[0].strip()
                except:
                    img=""
                print("img==",img)

                #获取产品链接
                link = tr.xpath("//a/@href")
                try:
                    link="https://www.ozon.ru"+link[0]
                except:
                    link=""
                print("link==", link)

                #获取产品ID
                mo = re.compile(r"\d{9}")
                try:
                    pro_id = mo.findall(link)[0]
                except:
                    pro_id=""
                print("pro_id=",pro_id)

                #获取价格
                price = tr.xpath('//div/div/div/span/text()')
                try:
                    price=price[0].split("₽")[0].strip()
                except:
                    price=0
                print("价格==",price)

                #获取评论数
                c_number = tr.xpath('//div[1]/div[2]/a/text()')
                try:
                    c_number=c_number[0].split("о")[0].strip()
                except:
                    c_number=0
                print("c_number==",c_number)

                #获取评分
                score = tr.xpath('//div[1]/div[2]/div/div/div[2]/@style')
                try:
                    score = score[0].split(":")[1][:-2]
                except:
                    score=0
                print("score==",score)

                #获取卖家名
                seller = tr.xpath('//div[1]/div[3]/div/span/span/text()')
                try:
                    seller=seller[0].split("продавец")[1].strip()
                except:
                    seller=""
                print("seller==",seller)
                item_data=[pro_id,img,price,c_number,score,seller,link]
                item_datas.append(item_data)
                print("\n\n\n")

        except:
            continue

    items_s=list(set(items_s))
    print("保存数据",item_datas)
    wt_csv(data=item_datas,mod="a")
    print("执行完find_next")
    return items_s,pags

def wt_csv(data,mod):
    with open("./test.csv",mod,newline="",encoding="utf-8-sig") as f:
        wt=csv.writer(f)
        wt.writerows(data)

if __name__=="__main__":
    #data = find_full("https://www.ozon.ru/product/top-bra-top-koda-1-sht-392616069/?_bctx=CAYQsOMa&asb=ddGi5oL7010qNn%252Fh%252FimVwJFftDdIEsmY%252BQYonWkjO5%252BzW8E0DoIBpQ%252FEpUFkgNwp&asb2=Lt5yB3LyF3MavtSP7_e6p4i99EL-mZNFnLOK4sYGTzrR2ouW3eHnGZ0vWOZNakEfBtEHijAVYCoL1TSX4GYUCf9GqPDRIyrlg5frEIv7A44237jWi_r5ncwU88eVWDgosuAexkT2G4mseVwOk2SZKw&sh=sgfh0CNUyg")

    #pag="https://www.ozon.ru/highlight/autlet-438704/?departurecountry=156"
    ''' '''
    pag="https://www.ozon.ru/highlight/autlet-438704/?category=7500&departurecountry=156"
    #pag="https://www.ozon.ru/highlight/autlet-438704/?category=7500&departurecountry=156&page=5"
    wt_csv(data=[["pro_id","img","price","c_number","score","seller","link"]],mod="w")
    while True:
        n = 0
        try:
            print("打算采集==",pag)
            items, pags = find_next(pag)
            print("pags==", pags)
            print("pag==", pag)
            if len(items)==0:
                if len(pags)==0:
                    n=n+1
                    if n>5:
                        pags=[]
                    else:
                        continue
                else:
                    print("很好，继续执行")
            n = 0
        except Exception as e:
            print("重试", n,e)
            n = n + 1
            if n > 10:
                break
            else:
                continue
        newpags=[]#去掉参数的产品列表url
        for np in pags:
            newpags.append(getnewpags(np))
        if "page=" not in pag:
            pag=pag+"&page=1"
            print("pag+&page=1==",pag)
            if pag not in pags:
                pag=pags[0]
        pag=pags[newpags.index(getnewpags(pag)) + 1]
        print("\n\n")
    ''' '''
