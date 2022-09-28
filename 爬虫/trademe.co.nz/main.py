import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Manager, Value, Pool, Queue
from concurrent.futures import ProcessPoolExecutor
import csv
def get_ip():
    #获取代理ip地址
    url="http://api2.xkdaili.com/tools/XApi.ashx?apikey=XK0F329BE981ECF21718&qty=1&format=json&split=0&sign=fecf58a89e3e2c2ccb56e7d5a02a5757"
    reg=requests.get(url)
    s=reg.text
    ips=eval(s)
    ls_ip=[]
    for i in ips["data"]:
        ip=i["ip"]
        port=i["port"]
        ls_ip.append(ip+":"+port)
    return ls_ip

def get_ips(ips):
    #获取到到ip地址放入ips这个通道
    print("打算获取ip==",ips.qsize())
    if ips.qsize()<2:
        print("开始获取ip")
        for ip in get_ip():
            ips.put([ip, 0, 0])
    #time.sleep(3)
    ls_ip = ips.get()
    return ls_ip

def find_html(url,ip,c):
    #获取网页源码
    if c=="":
        cookie = 'ajs_anonymous_id=ce158167-46fe-41f4-acbb-62beececc718; trademeclientid=7035fa4b-3dab-e7d4-eca6-d76e42312136; _gcl_au=1.1.798501655.1664112804; _gid=GA1.3.1325061753.1664112805; __gads=ID=2fc193d78d3d5a73:T=1664112805:S=ALNI_MYGknYJU9kghaTDR3aG6EjkkZH_-w; __gsas=ID=461455271618bb0d:T=1664113181:S=ALNI_MbU6BLbSUZ7x5oA5URkCoeARAqbTQ; jsValidationToken=9bd35c20-a7f2-46bb-a064-8198321b7215; _mkto_trk=id:890-UMT-461&token:_mch-trademe.co.nz-1664285388009-21519; session={59A6F583-262E-4D3E-9B2C-E6D448B15345}; _ga=GA1.3.2113871480.1664112804; __gpi=UID=000008c90777d4d1:T=1664112805:RT=1664289822:S=ALNI_MZjWcykV0CCH0t8QpoGGIg45mQPsA; _ga_JJTLVXMBWX=GS1.1.1664282580.7.1.1664289834.49.0.0; tm.FrEnd.browserSize=320'
    else:
        cookie=c
    headers = {
        "cookie": cookie,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }
    proxy = {
        "http": "http://{ip}".format(ip=ip),
        "https": "http://{ip}".format(ip=ip),
    }
    print("proxy==",proxy)
    reg = requests.get(url=url, proxies=proxy, headers=headers, timeout=5)

    return reg.text,reg.status_code

def find_title(bs_html):
    title = bs_html.select("h1")[0].getText().strip()
    return title
def find_closesTime(bs_html):
    s=bs_html.select(".tm-closing-datetime__small")[0].getText().strip()
    return s

def find_watchlisted(bs_html):
    n=bs_html.select(".tm-marketplace-buyer-options__watchers-count>strong")[0].getText().strip()
    return n

def find_price(bs_html):
    price_bs=bs_html.select(".tm-buy-now-box__price>strong")
    if price_bs==[]:
        price_bs = bs_html.select(".h-text-align-center>strong")
    price = price_bs[0].getText().strip()
    return price
def find_PageViews(bs_html):
    page=bs_html.select("tm-share-listing-link>div>b")[0].getText().strip()
    return page

def find_item(ips,url,qdata,c):
    n=0
    while True:
        n=n+1
        ls_ip = get_ips(ips)  # 获取代理
        print(ls_ip)
        if ls_ip[1]>5:
            print("重新获取")
            continue
        try:
            html, code = find_html(url=url, ip=ls_ip[0],c=c)
        except Exception as e:
            print(e)
            #没有获取到正确数据 进行重试操作
            ls_ip[1] = ls_ip[1] + 1
            ips.put(ls_ip)
            continue
        print("code==", code)
        print("html==", len(html))
        bs_html = BeautifulSoup(html, 'html.parser')
        #开始采集相关数据
        print("url=",url)
        try:
            title = find_title(bs_html=bs_html)
        except Exception as e:
            print("没获取到标题",e)
            title=""
        print("title==", title)
        try:
            cTime=find_closesTime(bs_html=bs_html)
        except Exception as e:
            print("关闭时间",e)
            cTime=""
        print("cTime=",cTime)
        try:
            watchlisted=find_watchlisted(bs_html=bs_html)
        except Exception as e:
            print("没找到watchlisted",e)
            watchlisted=0
        print("watchlisted==",watchlisted)
        try:
            price=find_price(bs_html=bs_html)
        except Exception as e:
            print("没获取到价格",e)
            price=0
        print("price==",price)
        try:
            page=find_PageViews(bs_html=bs_html)
        except Exception as e:
            print("没获取到page",e)
            page=""
        print("page=",page)
        ls_ip[2] = ls_ip[2] + 1
        ips.put(ls_ip)
        #data=[title,cTime,watchlisted,price,page,url]
        data={
            'A': title,
            'B': cTime,
            'C': watchlisted,
            'D': price,
            'E': page,
            'F':url,
            }
        print("成功采集入:",data)
        qdata.put(data)
        print("\n\n")
        break

def find_itemurl_nextpage(ips,purl,c):
    while True:
        ls_ip = get_ips(ips)
        print(ls_ip)
        if ls_ip[1]>5:
            print("重新获取")
            continue
        print("开始采集", purl)
        try:
            html, code = find_html(url=purl, ip=ls_ip[0],c=c)
        except Exception as e:
            print("获取html失败", e)
            ls_ip[1] = ls_ip[1] + 1
            ips.put(ls_ip)
            continue
        print(len(html),code)
        if len(html)<100000:
            print("重试")
            ls_ip[1] = ls_ip[1] + 1
            ips.put(ls_ip)
            continue
        bs_html = BeautifulSoup(html, 'html.parser')
        itemurl = bs_html.select(".o-card>a")
        pro_urls = []
        for item in itemurl:
            pro_url = "https://www.trademe.co.nz/a/" + item['href'].split("?")[0]
            pro_urls.append(pro_url)
            # find_item(ips=ips,url=pro_url)
        nextpage = bs_html.select(".o-pagination__link>a")
        npurl = ""
        for i in nextpage:
            if i.getText().strip() == "Next":
                npurl = "https://www.trademe.co.nz" + i['href']
        # 采集成功,把ip地址放入池子
        ls_ip[2] = ls_ip[2] + 1
        ips.put(ls_ip)
        break
    return pro_urls,npurl

if __name__ == '__main__':

    #purl="https://www.trademe.co.nz/a/marketplace/baby-gear"
    purl=input("请输入要采集的产品类目url:").strip()
    str_num=input("请输入线程数(默认5):").strip()
    c=input("请输入cookie(可选):").strip()
    if r'"' in purl:
        purl=purl.replace(r'"','')
    f_name=purl.split(r'/')[-1]
    csv_path = "./" + f_name + ".csv"
    if str_num=="":
        ThNum=5
    else:
        ThNum=int(str_num)

    ips = Manager().Queue(maxsize=0)
    # 写入表头
    head_csv = {
        'A': 'Title',
        'B': 'Closes',
        'C': 'Watchlisted',
        'D': 'Price',
        'E': 'Page views',
        'F':'Url'
    }
    with open(csv_path, "w", encoding='utf8', newline='') as f:
        f_csv = csv.DictWriter(f, head_csv)
        f_csv.writerow(head_csv)

    while True:
        pro_urls, npurl=find_itemurl_nextpage(ips=ips,purl=purl,c=c)
        print("pro_urls==",pro_urls)
        print("npurl==",npurl)
        q_datas = Manager().Queue() #用来装数据
        p = ProcessPoolExecutor(max_workers=ThNum)  # 创建一个进程池
        for url in pro_urls:
            #find_item(ips=ips,url=url)
            p.submit(find_item,ips,url,q_datas,c)
        p.shutdown()
        print("数据量==",q_datas.qsize())
        items=[]
        while q_datas.qsize()>0:
            data=q_datas.get()
            print("成功",data)
            items.append(data)

        with open(csv_path, "a", encoding='utf8', newline='') as f:
            f_csv = csv.DictWriter(f, head_csv)
            for i in items:
                f_csv.writerow(i)
        if npurl=="":
            print("采集完毕")
            break
        purl=npurl
        continue
