# -*- coding: utf-8 -*- 
import logging
import requests
import time
import bs4
import re
import json
import csv
import lxml
from multiprocessing import Process,Queue
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from datetime import datetime
import os,time

#重新拨号
def restartADSL():
    import os
    import time
    os.system('pppoe-stop')
    time.sleep(10)
    os.system('pppoe-start')
    time.sleep(10)

def find_bs(url,headers):
    try:
        r = requests.get(url,timeout=10,headers=headers)
    except Exception as e:
        print('请求问题:{e}'.format(e=e))
        return find_bs(url,headers)
    n=r.status_code
    print('返回状态{}'.format(n))
    if n!=200:
        print("返回状态码为{},重新链接".format(n))
        return find_bs(url,headers)
    html=r.text
    print('html:',len(html))
    '''
    if len(html)<7000:
        print("find_bs，被网站屏蔽，手动抛出异常")
        raise NameError
    '''
    bs=bs4.BeautifulSoup(html,'lxml')
    if bs.select("h2")==[]:
        print('没找到h2,继续尝试')
        return find_bs(url,headers)
    return bs

#获取下一个页面以及本页面的产品URL
def find_page_url(bs):
    asins=find_page_pro_url(bs)
    try:
        next_url=bs.select(".a-last a")
    except Exception as e:
        print("没匹配到.a-last a",e)
        raise NameError
    for i in next_url:
        page_url="https://www.amazon.com"+i.get("href")
    return page_url,asins

#获取页面的所有产品url
def find_page_pro_url(bs):
    try:
        h2=bs.select('h2 a')
    except Exception as e:
        print(r"没有找到'h2 a'",e)
        raise NameError
    asins=[]
    for i in h2:
        url=i.get("href")
        #获取asin
        mo=re.compile("\/dp\/.*\/ref=")
        try:
            asin=mo.findall(url)[0][4:-5]
        except Exception as e:
            print('跳过',e)
            continue
        print(asin)
        asins.append(asin+'\n')
    print('asins:',len(asins))
    return asins
#写入txt
def write_txt(s,path):
    with open(path,"a",encoding="utf8",newline="") as f:
        f.write(s)

def loads_str(data_str):
    #data_str=re.sub('\'','\"',data_str)
    try:
        result = json.loads(data_str)
        #print("最终json加载结果：{}".format(result))
        return result
    except Exception as e:
        #print("异常信息e：{}".format(e))
        error_index = re.findall(r"char (\d+)\)", str(e))
        if error_index:
            error_str = data_str[int(error_index[0])]
            data_str = data_str.replace(error_str, "<?>")
            #print("替换异常字符串{} 后的文本内容{}".format(error_str, data_str))
            #该处将处理结果继续递归处理
            return loads_str(data_str)

def ipip():
    try:
        req=requests.get("http://txt.go.sohu.com/ip/soip",timeout=10).text
        ips=re.findall (r'\d+.\d+.\d+.\d+',req)
        return ips[0]
    except Exception as e:
        return "IP查询失败{e}".format(e=e)

def find_des(bs):
    dess=bs.select(".a-unordered-list.a-vertical.a-spacing-mini li span")
    de=[]
    for des in dess:
        de.append(des.getText())
    return "".join(de)

def find_title(bs):
    title=bs.select("title")
    title=title[0].getText()[12:]
    return title

def find_price(bs):
    price=bs.select(".a-size-medium.a-color-price")
    p=price[0].getText()
    if r"$" not in p:
        price2=bs.select(".a-size-base.a-color-price")
        p=price2[0].getText()
    p=p.strip()
    p=re.sub(r"$",'',p)
    return p

def okpage(bs):
    #判断返回的页面是否正常
    ok=bs.select(".a-fixed-left-grid")
    if ok==[]:
        return False
    else:
        return True

def find_pro_bs(asin,headers):  
    url=r"https://www.amazon.com/dp/"+asin
    print("请求IP:",ipip())
    print("请求页面",url)
    r = requests.get(url,timeout=10,headers=headers)
    if r.status_code != 200:
        find_pro_bs(asin,headers)
    html=r.text
    html=str(html)
    print('html:',len(html))
    bs=bs4.BeautifulSoup(html,'lxml')
    return bs,html

def find_pro_1(asin,head_csv,headers,t,q,csv_path):
    #初始化表格，设置某个一字段都为空
    csv_row=head_csv.copy()
    for i in csv_row:
        csv_row[i]=''
    url_pro=asin+"?th=1&psc=1"
    
    bs,html=find_pro_bs(url_pro,headers)
    if okpage(bs)==False:
        restartADSL()
        t=t-1
        if t > -10:
            find_pro_1(asin,head_csv,headers,t,q,csv_path)
        else:
            raise EOFError

    title=find_title(bs)
    try:
        price=find_price(bs)
    except Exception as e:
        print(r"单体商品价格转换失败",e)
        price=0
    des=find_des(bs)
    try:
        mo2=re.compile("\'colorImages\':.*")
        #可以获取单个产品的所有图片
    except Exception as e:
        print(r"没有找到'colorImages':",e)
        raise NameError
    js_d=mo2.findall(html)[0]
    js_d=js_d[28:-2]
    d=loads_str(js_d)
    #图片
    pic=[]
    d_csv=[]
    for i in d:
        pic.append(i["hiRes"])
        break
    csv_row['B']='simple'#默认单品
    csv_row['C']=asin
    csv_row['D']=title
    csv_row['E']='1'
    csv_row['F']='0'
    csv_row['G']='visible'
    csv_row['I']=des
    csv_row['L']='taxable'
    csv_row['N']='1'
    csv_row['AQ']='0'
    csv_row['AW']='1'
    csv_row['Z']=price
    csv_row['AA']='SEOTYPE'
    csv_row['AB']='SEOTAGE'
    csv_row['AD']=','.join(pic)
    csv_row['AN']='Size'
    csv_row['AP']='1'
    csv_row['AR']='Color'
    csv_row['AU']='0'
    d_csv.append(csv_row)
    #把结果写入队列
    print('采集结果',csv_row)
    wt_csv(d_csv,csv_path)

def wt_csv(d_csv,csv_path):
    with open(csv_path,"a",encoding='utf8',newline='') as f:
        f_csv=csv.DictWriter(f,head_csv)
        for i in d_csv:
            f_csv.writerow(i)
    print('成功写入')

def production(asin_path,q,csv_path):
    p=ProcessPoolExecutor(max_workers=25) #创建一个进程池
    with open(asin_path,'r',encoding='utf8') as f:
        for asin in f:
            asin=re.sub("\n",'',asin)
            #采集单品并写入队列
            p.submit(find_pro_1,asin,head_csv,headers,t,q,csv_path)  # 往进程池内提交任务
            time.sleep(1)

def consumption(csv_path,q):
    d_csv=q.get()
    print('取出的内容',d_csv)
    wt_csv(d_csv,csv_path)


if __name__ =="__main__":
    #程序主体部分
    head_csv={'A': 'ID', 'B': 'Type', 'C': 'SKU', 'D': 'Name', 'E': 'Published', 'F': 'Is featured?', 'G': 'Visibility in catalog', 'H': 'Short description',
            'I': 'Description', 'J': 'Date sale price starts', 'K': 'Date sale price ends', 'L': 'Tax status', 'M': 'Tax class', 'N': 'In stock?', 'O': 'Stock',
            'P': 'Low stock amount', 'Q': 'Backorders allowed?', 'R': 'Sold individually?', 'S': 'Weight (kg)', 'T': 'Length (cm)', 'U': 'Width (cm)', 
            'V': 'Height (cm)', 'W': 'Allow customer reviews?', 'X': 'Purchase note', 'Y': 'Sale price', 'Z': 'Regular price', 'AA': 'Categories', 'AB': 'Tags', 
            'AC': 'Shipping class', 'AD': 'Images', 'AE': 'Download limit', 'AF': 'Download expiry days', 'AG': 'Parent', 'AH': 'Grouped products', 'AI': 'Upsells', 
            'AJ': 'Cross-sells', 'AK': 'External URL', 'AM': 'Button text', 'AL': 'Position', 'AN': 'Attribute 1 name', 'AO': 'Attribute 1 value(s)', 
            'AP': 'Attribute 1 visible', 'AQ': 'Attribute 1 global', 'AR': 'Attribute 2 name', 'AS': 'Attribute 2 value(s)', 'AT': 'Attribute 2 visible', 
            'AU': 'Attribute 2 global', 'AV': 'Meta: pf_size_chart', 'AW': 'Meta: _primary_term_product_cat'
            }
    headers= {
            'Accept-Language':'en-us,en;q=0.9',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'cookie':r'session-id-time=2082787201l; session-id=143-7283193-0434042; ubid-main=135-4071739-0100158; i18n-prefs=USD; session-token=F1LPasjCZIhIQ3/UGQzCK5nsUrdENnnmnEtR39OUktmBknNz2vdXXWxPOt7TEoa6vmDlLxrS6DtUP45Q//el4TorL3P/dxmPofxCIQNxJTdAm4VegAQpnjMFvd1iytSxmCo8A8EpGmHFurR6fehGlCCvQl1+XDM9qcGXvlg6bdKcz2LQv0xkdqye+tM3mHl+vQ8A39yGrNXr0Zdf0zh4t5AWSZAEtibFA7ijzLXESlwl85N8bV4MacnWQl46mWYM; csm-hit=tb:s-M0ECGT4J6MCDVSNCDN6F|1601001176170&t:1601001180260&adb:adblk_no'
            }
    #相关设置
    url='https://www.amazon.com/s?k=phone+case&rh=p_72%3A2661618011%2Cp_n_feature_nine_browse-bin%3A21217139011&dc&qid=1602829027&rnid=2488708011&ref=sr_nr_p_n_feature_nine_browse-bin_3'
    csv_path=r"./test.csv"

    asin_path=r'./asin.txt'#可不修改
    t=5

    #采集asin
    while True:
        asin=''
        try:
            #获取下一页url和本页面的产品url
            bs=find_bs(url,headers)
            print('成功获取bs')
            page_url,asins=find_page_url(bs)
            print('成功获取产品asin和下一页')
            str_asins="".join(asins)
            write_txt(str_asins,asin_path)
            print("page_url-----",page_url)
            print("asins------",str_asins)

        except Exception as e:
            print(e)
            print("采集完毕！")
            print("最后采集页面是",url)
            break
        url=page_url

    #写入表头
    with open(csv_path,"w",encoding='utf8',newline='') as f:
        f_csv=csv.DictWriter(f,head_csv)
        f_csv.writerow(head_csv)

    #创建队列
    q = Manager().Queue()
    #创建进程
    production(asin_path,q,csv_path).start() #生产
    #consumption(csv_path,q).start() #消费
    print('采集完毕')
