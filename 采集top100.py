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

#获取top100产品asin
def find_hot_asin(bs):
    hot_asin=bs.select('a.a-link-normal')
    asins=[]
    for i in hot_asin:
        asin=i.get('href')
        if r'/dp/' in asin:
            #print('原始asin:',asin)
            mo=re.compile("\/dp\/.*\/ref=")
            try:
                asin=mo.findall(asin)[0][4:-5]
            except Exception as e:
                print(e)
                continue
            #print('处理后的asin----',asin)
            asins.append(asin)
    return list(set(asins))

#获取下一页url
def find_next_page(bs):
    next_page=bs.select('.a-last a')[0].get('href')
    return next_page

#生成器
def find_x():
    a=0
    while True:
        yield a
        a=a+1
#写入txt
def write_txt(s,path):
    with open(path,"a",encoding="utf8",newline="") as f:
        f.write(s)

def find_bs(url,headers):
    r=connect(url,headers)
    n=r.status_code
    print('返回状态{}'.format(n))
    html=r.text
    bs=bs4.BeautifulSoup(html,'lxml')
    return bs

def okpage(bs):
    #判断返回的页面是否正常
    ok=bs.select(".a-fixed-left-grid")
    if ok==[]:
        return False
    else:
        return True
#重新拨号
def restartADSL():
    import os
    import time
    os.system('pppoe-stop')
    time.sleep(3)
    os.system('pppoe-start')
    time.sleep(3)

def find_price(bs):
    price=bs.select(".a-size-medium.a-color-price")
    p=price[0].getText()
    if r"$" not in p:
        price2=bs.select(".a-size-base.a-color-price")
        p=price2[0].getText()
    p=p.strip()
    p=re.sub(r"$",'',p)
    return p

def find_title(bs):
    title=bs.select("title")
    title=title[0].getText()[12:]
    return title

def find_des(bs):
    dess=bs.select(".a-unordered-list.a-vertical.a-spacing-mini li span")
    de=[]
    for des in dess:
        de.append(des.getText())
    return "".join(de)

def ipip():
    try:
        req=requests.get("http://txt.go.sohu.com/ip/soip",timeout=10).text
        ips=re.findall (r'\d+.\d+.\d+.\d+',req)
        return ips[0]
    except Exception as e:
        return "IP查询失败{e}".format(e=e)

def find_d_c(html):
    try:
        mo2=re.compile("\'colorImages\':.*")
        #可以获取单个产品的所有图片
    except Exception as e:
        print(r"没有找到'colorImages':",e)
        raise NameError
    js_d=mo2.findall(html)[0]
    js_d=js_d[28:-2]
    d=loads_str(js_d)
    return d

def find_pic(d):
    pic=[]
    for i in d:
        p=i["hiRes"]
        if p!=None:
            #print('p----',p)
            pic.append(p)
    return pic

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

def connect(url,headers):
    print("链接页面",url)
    #print("请求IP:",ipip())
    r = requests.get(url,timeout=10,headers=headers)
    okcode=r.status_code
    print('返回状态:',okcode)
    return r

def find_pro_bs(asin,headers):
    url=r"https://www.amazon.com/dp/"+asin
    r =connect(url,headers)
    html=r.text
    html=str(html)
    print('html:',len(html))
    bs=bs4.BeautifulSoup(html,'lxml')
    return bs,html

def find_pro_bs_n(asin,headers):  
    url="https://www.amazon.com/dp/{asin}?th=1&psc=1".format(asin=asin)
    r = connect(url,headers)
    html=r.text
    html=str(html)
    bs=bs4.BeautifulSoup(html,'lxml')
    return bs,html

#采集变体    
def find_pro_n(asin,js_d,head_csv,headers,q,t,q_asin):
    print('开始采集变体',asin)
    #初始化表格，设置某个一字段都为空
    csv_row=head_csv.copy()
    for i in csv_row:
        csv_row[i]=''
    #寻找变体bs,递归重试
    bs,html=find_pro_bs_n(asin,headers)
    ok=bs.select(".a-fixed-left-grid")
    if ok==[]:
        raise NameError
    title=find_title(bs)
    try:
        price=find_price(bs)
        print('商品价格为{p}'.format(p=price))
    except Exception as e:
        print(r"转换价格失败",e)
        price=0
    try:
        color=js_d[asin][1]
        print('颜色是{c}'.format(c=color))
    except Exception as e:
        print('采集颜色失败',e)
        color=''
    csv_row['C']=asin
    csv_row['D']=title
    csv_row['E']='1'
    csv_row['F']='0'
    csv_row['G']='visible'
    csv_row['I']=find_des(bs)
    csv_row['L']='taxable'
    csv_row['N']='1'
    csv_row['O']='100'
    csv_row['Q']='0'
    csv_row['R']='0'
    csv_row['W']='1'
    csv_row['Z']=price
    csv_row['AA']='SEOTYPE'
    csv_row['AB']='SEOTAGE'
    #获取图片
    d_c=find_d_c(html)
    #print('d_c----',d_c)
    pic=','.join(find_pic(d_c))
    #print('pic----',pic)
    csv_row['AD']=pic
    csv_row['AP']='1'
    csv_row['AT']='1'
    csv_row['AR']='Opt'
    csv_row['AS']=color
    csv_row['AN']='Opt'
    csv_row['AO']=js_d[asin][0]
    csv_row['AQ']='0'
    csv_row['AU']='0'
    print('采集完变体',asin)
    q.put(csv_row)
    q_asin.put(asin)

#采集单品
def find_pro_1(asin,head_csv,d_csv,headers,t):
    #初始化表格，设置某个一字段都为空
    csv_row=head_csv.copy()
    for i in csv_row:
        csv_row[i]=''
    url_pro=asin+"?th=1&psc=1"
    bs,html=find_pro_bs(url_pro,headers)
    if okpage(bs)==False:
        restartADSL()
        t=t-1
        if t > 0:
            print('重新执行find_pro(),剩余尝试次数为---{t}'.format(t=t))
            find_pro_1(asin,head_csv,d_csv,headers,t)
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
        #没有发现图片则终止该进程
        raise NameError
    js_d=mo2.findall(html)[0]
    js_d=js_d[28:-2]
    d=loads_str(js_d)
    #图片
    pic=[]
    for i in d:
        pic.append(i["hiRes"])
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

def find_pro(csv_path,main_asin,headers,head_csv,t,q_asin,q_asin_list,q,q_asins,all_asin,max_asin):
    #设置主asin
    main_asin=main_asin
    #如果得不到要的内容则重新拨号
    bs1,html=find_pro_bs(main_asin,headers)
    if okpage(bs1)==False:
        restartADSL()
        t=t-1
        if t > 0:
            print('重新执行find_pro(),剩余尝试次数为---{t}'.format(t=t))
            find_pro(csv_path,main_asin,headers,head_csv,t,q_asin,q_asin_list,q,q_asins,all_asin,max_asin)
        else:
            raise EOFError
    try:
        mo_d=re.compile("\"dimensionValuesDisplayData\" : .*")
        js_d=mo_d.findall(html)
        #js_d={"B085SZST1L":["Small","No.24"],"B085SX1PRG":["3X-Large","Cobra"]}
        #包括了asin,和规格（大小，颜色）
    except Exception as e:
        print("没匹配到dimensionValuesDisplayData",e)#意味着这个商品是单品
        js_d=[]
    #初始化一个值为空字符串的字典
    csv_row=head_csv.copy()
    for i in csv_row:
        csv_row[i]=''
    if js_d!=[]:
        print('采集相关变体',r"https://www.amazon.com/dp/"+main_asin)
        js_d=js_d[0][30:-1]
        #把字符串转换为字典
        js_d=loads_str(js_d)
        #获取所有size
        try:
            sizes=[i[0] for i in list(js_d.values())]
        except Exception as e:
            print("获取所有size失败",e)
            sizes=[]
        #获取所有颜色
        try:
            colors=[i[1] for i in list(js_d.values())]
        except Exception as e:
            print('没有发现颜色',e)
            colors=[]
        if len(all_asin)==0:
            #获取所有all_asin
            all_asin=[asin for asin in js_d]
            #去重
            all_asin=list(set(all_asin))
            print('变体总数:',len(all_asin))
        #设置采集最大变体数
        if max_asin == -1:
            pass
        elif len(all_asin) >= max_asin:
            all_asin=all_asin[:max_asin]
        print('实际要采集的变体总数:',len(all_asin))
        #设置一个列表用来装商品及其变体
        d_csv=[]
        if len(all_asin)==1:
            #采集单品
            find_pro_1(main_asin,head_csv,d_csv,headers,t)
        else:
            p=ProcessPoolExecutor(max_workers=20)  # 创建一个进程池
            n=0
            print('打算创建线程')
            for asin in all_asin:
                if asin in q_asin_list:
                    print(asin,'已经采集过')
                    continue
                try:
                    p.submit(find_pro_n,asin,js_d,head_csv,headers,q,t,q_asin)  # 往进程池内提交任务
                    time.sleep(1)
                except:
                    print('启动失败')
                print("启动进程{n}".format(n=n))
                n=n+1
            p.shutdown() #主进程等待子进程结束
            print("--------------所有子进程处理完毕！------------")
            print('队列中内容量',q.qsize(),'实际要采集的数量',len(all_asin))
            if len(all_asin) != q.qsize():
                print("重新拨号，重新采集")
                restartADSL()
                #获取成功采集产品的数量
                qn=q_asin.qsize()
                print('成功采集的数量-------------------',qn,'实际要采集的数量-------',len(all_asin))
                #把q_asin中的asin全部取出并放入q_asin_list中
                while q_asin.empty()==False:
                    try:
                        #把q_asin中的内容取出
                        x=q_asin.get()
                        #把队列中的内容写入已采集列表
                        print("把队列q_asin中asin{x}写入已采集列表,当前数量为{n}".format(n=q_asin.qsize(),x=x))
                        #取出的asin只有存在于原asin列表中，才写入待采集列表
                        if x in all_asin:
                            q_asin_list.add(x)
                            #把q_asin中的内容给q_asins
                            print("把q_asin中的内容给q_asins")
                            q_asins.put(x)
                    except Exception as e:
                        print(e)

                #再把q_asins还给q_asin
                print('再把q_asins还给q_asin')
                while q_asins.empty()==False:
                    try:
                        q_asin.put(q_asins.get())
                    except Exception as e:
                        print(e)
                #再次采集
                print('再次采集')
                find_pro(csv_path,main_asin,headers,head_csv,t,q_asin,q_asin_list,q,q_asins,all_asin,max_asin)

            #把队列q中的内容全部取出，放入d_csv
            while q.empty()==False:
                d_csv.append(q.get())
            print('成功把q中的内容写入d_csv,并清空q')

            #清空q_asin
            while q_asin.empty()==False:
                q_asin.get()
            #清空all_asin
            all_asin.clear()

            #设置默认商品
            print('设置默认商品')
            if len(d_csv)==1:
                for r in d_csv:
                    r['B']='simple'#默认单品
                #以单品设置表格
                pass
            elif len(d_csv)>1:
                #设置两个空列表用来装变体属性
                aos=[]
                ass=[]
                for i in d_csv:
                    aos.append(i['AO'])
                    ass.append(i['AS'])
                #设置默认商品
                df=d_csv[0].copy()
                #设置默认商品的属性
                df['B']='variable'
                df['C']=main_asin
                df['M']=''
                df['Z']=''
                df['AA']='SEOTYPE'
                df['AB']='SEOTAGE'
                df['AG']=''
                if len(sizes)==0:
                    df['AN']=''
                    df['AO']=''
                else:
                    df['AN']='Opt'
                    df['AO']=','.join(aos)
                    #清空aos
                    aos.clear()
                if len(colors)==0:
                    df['AR']=''
                    df['AS']=''
                else:
                    df['AR']='Opt'
                    df['AS']=','.join(ass)
                    ass.clear()
                df['AT']='1'
                
                #设置变体
                for r in d_csv:
                    #设置变体
                    r['B']='variation'
                    r['I']=''
                    r['M']='parent'
                    r['O']=''
                    r['AG']=main_asin
                    r['AP']=''
                    r['AT']=''
                    if len(sizes)==0:
                        r['AN']=''
                        r['AO']=''
                    if len(colors)==0:
                        r['AR']=''
                        r['AS']=''
        if len(d_csv)==0:
            pass
        else:
            #把默认商品插入到商品列表中第一个
            d_csv.insert(0,df)

            print('最终d_csv---',d_csv)
            with open(csv_path,"a",encoding='utf8',newline='') as f:
                f_csv=csv.DictWriter(f,head_csv)
                for i in d_csv:
                    f_csv.writerow(i)
            print("成功写入{asin}到{csv_path}".format(asin=main_asin,csv_path=csv_path))
            d_csv.clear()
            q_asin_list.clear()
    else:
        #采集单品
        print('采集单品')
        #设置一个列表用来装商品数据
        d_csv=[]
        find_pro_1(main_asin,head_csv,d_csv,headers,t)
        if len(d_csv)==0:
            pass
        else:
            print('最终d_csv---',d_csv)
            with open(csv_path,"a",encoding='utf8',newline='') as f:
                f_csv=csv.DictWriter(f,head_csv)
                for i in d_csv:
                    f_csv.writerow(i)
            print("成功写入{asin}到{csv_path}".format(asin=main_asin,csv_path=csv_path))
            d_csv.clear()
            q_asin_list.clear()

def find_pro_ite(ite,url,m_page,max_asin):
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
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'cookie':r'i18n-prefs=USD; ubid-main=131-0057010-7295530; session-id=137-3981079-4674212; s_fid=1F47EF4C579A7112-100EF923F5428714; lc-main=en_US; aws-priv=eyJ2IjoxLCJldSI6MCwic3QiOjB9; aws-target-static-id=1594282266887-799918; aws-target-data=%7B%22support%22%3A%221%22%7D; regStatus=pre-register; aws-target-visitor-id=1594282266891-720092.38_0; s_vn=1625818267214%26vn%3D2; s_dslv=1594286431252; x-main="ILesnhQ98zJUb0Whkh1xjuU@Y5ZUbQzysaUOtN1YdEJo09CekkkGDtftI4mF4hd3"; at-main=Atza|IwEBIKbS6wo9mxjbTClyslIU4kJWv8smNIls8RQlvYUDO1qqXRm55rC5o4Lh6RFsKoXml12UanotvBHwb4584MYxB9ucbcpreArK3uxoHo7eAkEx7VSkMkuYxCkNZzySM25bRJf0Zw80cR2pzMqiwSHp6q1FhvLkUrvlidEJep5FvSu1vlWJaEtEmtSQ-k7574i_n5nErE00o3NRygaKLyhTMjDt; sess-at-main="V7Ggy9q3BQXrFfa2Ir3WfWGAoHqSY/jqAS//c0sW248="; sst-main=Sst1|PQFN8S1N0HsDYQ9e5pLbcMGmC6i746Lu543nYOw7Kq7butaC0Dxglc-NZ1jt6Sfl6WpsFlh54xmnxc8mFqBcW68CZWgGj2wNgipZbas4R-TMkLYWF4sMoAscHgIjp6hvQ41us6VvPDh3PLpLoJDclLZzN3vsKsNCegDNXnauBAHjJfI5BOFS5Noscv4e6FS1s9iNxDnfnCwPP_AjcxTCHpgopQemIlC1QPYAj6iilbv6GHwpjMu2Z7QMy4_uLx7Jkn7pIhKjgdkyx34pL7fvZ3IsRmGRdWsxyPTXKwDQXWilt9yMRg4G5pk97lu1KRQmJK2dNbbb9Zl9qIfe-MVOWNvR8A; skin=noskin; session-token="Gsjx13DXYWg3Qh+30j8+3mPoFqBL0rmqQT+8mVaijuQDfpTRzPsUJ/i3J+qQ1fElEv0L4xD9QS9GMlyEsi2Lgs4KB/72YnKyqeqgM5nTt3OZoIaWoSyNxn7D9I8o7tcN0VNhYgPEWavqIF3ahZ7QHy2MnWYBzfLDIDA8mNJpBEFL2zKlInJHk8CrQCxRH5rAz8wUeWm3B6bkZ+DnzSqyRw=="; session-id-time=2082787201l; csm-hit=tb:E0HFRSJM79K8EYNF8E0X+s-E0HFRSJM79K8EYNF8E0X|1605602896438&t:1605602896438&adb:adblk_no'
            }
    #相关设置
    url=url
    csv_path="./pro/{ite}.csv".format(ite=ite)
    asin_path="./asin/{ite}.txt".format(ite=ite)#可不修改
    ok_asin="./ok_asin"
    t=100
    #采集asin
    while True:
        bs=find_bs(url,headers)
        #获取本页的所有产品asin
        asins=find_hot_asin(bs)
        for asin in asins:
            write_txt(asin+'\n',asin_path)
        #获取下一页url
        try:
            next_url=find_next_page(bs)
        except Exception as e:
            print('采集完毕',e)
            break
        url=next_url

    #写入表头
    with open(csv_path,"w",encoding='utf8',newline='') as f:
        f_csv=csv.DictWriter(f,head_csv)
        f_csv.writerow(head_csv)

    with open(asin_path,'r',encoding='utf8') as f:
        q_asin_list=set()
        all_asin=[]
        q_asins=Manager().Queue()
        q = Manager().Queue()
        q_asin=Manager().Queue()
        for asin in f:
            main_asin=re.sub("\n",'',asin)
            with open(ok_asin,'r') as f:
                red_ok_asin=f.read()
                if main_asin in red_ok_asin:
                    print('{main_asin}已存在,跳过'.format(main_asin=main_asin))
                    continue
            try:
                find_pro(csv_path,main_asin,headers,head_csv,t,q_asin,q_asin_list,q,q_asins,all_asin,max_asin)
                print('采集完{asin}'.format(asin=main_asin))
                write_txt(main_asin+'\n',ok_asin)
            except Exception as e:
                print('采集{asin}失败,跳过'.format(asin=main_asin),e)
                while q.empty()==False:
                    q.get()
                print('成功清空q')
                restartADSL()

if __name__ =="__main__":
    restartADSL()
    m_page=-1 #采集最大页数 -1为全部
    max_asin=11 #采集变体最大数 -1为全部
    with open('./urls','r',encoding='utf-8') as f:
        readCSV=csv.reader(f)
        for row in readCSV:
            ite=row[0]
            if '#' in ite:
                print('跳过{ite}'.format(ite=ite))
                continue
            url=row[1]
            find_pro_ite(ite,url,m_page,max_asin)
