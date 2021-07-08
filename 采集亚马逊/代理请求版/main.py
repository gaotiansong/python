# -*- coding: utf-8 -*- 
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

#生成器
def find_x():
    a=0
    while True:
        yield a
        a=a+1

#获取页面的所有产品asin
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

#获取下一个页面以及本页面的产品URL
def find_page_url(bs,asin_path):
    #获取asin并存入asin_path
    asins=find_page_pro_url(bs)
    str_asins="".join(asins)
    write_txt(str_asins,asin_path)
    try:
        next_url=bs.select(".a-last a")
    except Exception as e:
        print("没匹配到.a-last a",e)
        raise NameError
    for i in next_url:
        page_url="https://www.amazon.com"+i.get("href")
    return page_url,asins

#写入txt
def write_txt(s,path):
    with open(path,"a",encoding="utf8",newline="") as f:
        f.write(s)

def find_bs(url,headers,proxy):
    try:
        r = requests.get(url,timeout=10,proxies=proxy,headers=headers)
    except Exception as e:
        print('请求问题:{e}'.format(e=e))
        return find_bs(url,headers,proxy)
    n=r.status_code
    print('返回状态{}'.format(n))
    if n!=200:
        print("返回状态码为{},重新链接".format(n))
        return find_bs(url,headers,proxy)
    html=r.text
    print('html:',len(html))

    bs=bs4.BeautifulSoup(html,'lxml')
    if bs.select("h2")==[]:
        print('没找到h2,继续尝试')
        return find_bs(url,headers,proxy)
    return bs

def okpage(bs):
    #判断返回的页面是否正常
    ok=bs.select(".a-fixed-left-grid")
    if ok==[]:
        return False
    else:
        return True

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

def find_pro_bs(asin,proxy,headers):  
    url=r"https://www.amazon.com/dp/"+asin
    print("请求页面",url)
    r = requests.get(url,timeout=10,proxies=proxy,headers=headers)
    if r.status_code != 200:
        find_pro_bs(asin,proxy,headers)
    html=r.text
    html=str(html)
    print('html:',len(html))
    bs=bs4.BeautifulSoup(html,'lxml')
    return bs,html

def find_pro_bs_n(asin,proxy,headers,t):  
    url="https://www.amazon.com/dp/{asin}?th=1&psc=1".format(asin=asin)
    print("请求页面",url)
    r = requests.get(url,timeout=10,proxies=proxy,headers=headers)
    if r.status_code != 200:
        t=t-1
        if t >0:
            find_pro_bs_n(asin,proxy,headers,t)
        else:
            pass
    html=r.text
    html=str(html)
    bs=bs4.BeautifulSoup(html,'lxml')
    ok=bs.select(".a-fixed-left-grid")
    if ok==[]:
        print("没有找到.a-fixed-left-grid,结束该进程")
        raise NameError
    return bs,html
def find_pro_n(asin,js_d,head_csv,proxy,headers,q,t,q_asin):
    print('开始采集变体',asin)
    #初始化表格，设置某个一字段都为空
    csv_row=head_csv.copy()
    for i in csv_row:
        csv_row[i]=''
    #寻找变体bs,递归重试
    bs,html=find_pro_bs_n(asin,proxy,headers,t)
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


def find_pro_1(asin,head_csv,d_csv,proxy,headers,t):
    #初始化表格，设置某个一字段都为空
    csv_row=head_csv.copy()
    for i in csv_row:
        csv_row[i]=''
    url_pro=asin+"?th=1&psc=1"
    bs,html=find_pro_bs(url_pro,proxy,headers)
    if okpage(bs)==False:
        t=t-1
        if t > -10:
            find_pro_1(asin,head_csv,d_csv,proxy,headers,t)
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

def find_pro(csv_path,main_asin,proxy,headers,head_csv,t,q_asin,q_asin_list,q,q_asins,all_asin,max_asin):
    #设置主asin
    main_asin=main_asin
    #如果得不到要的内容则重新拨号
    bs1,html=find_pro_bs(main_asin,proxy,headers)
    if okpage(bs1)==False:
        t=t-1
        if t > 0:
            find_pro(csv_path,main_asin,proxy,headers,head_csv,t,q_asin,q_asin_list,q,q_asins,all_asin,max_asin)
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
            find_pro_1(main_asin,head_csv,d_csv,proxy,headers,t)
        else:
            p=ProcessPoolExecutor(max_workers=20)  # 创建一个进程池
            n=0
            print('打算创建线程')
            for asin in all_asin:
                if asin in q_asin_list:
                    print(asin,'已经采集过')
                    continue
                try:
                    p.submit(find_pro_n,asin,js_d,head_csv,proxy,headers,q,t,q_asin)  # 往进程池内提交任务
                    time.sleep(0)
                except:
                    print('启动失败')
                print("启动进程{n}".format(n=n))
                n=n+1
            p.shutdown() #主进程等待子进程结束
            print("--------------所有子进程处理完毕！------------")
            print('队列中内容量',q.qsize(),'实际要采集的数量',len(all_asin))
            if len(all_asin) != q.qsize():
                print("重新拨号，重新采集")
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
                find_pro(csv_path,main_asin,proxy,headers,head_csv,t,q_asin,q_asin_list,q,q_asins,all_asin,max_asin)
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
        d_csv=[]
        find_pro_1(main_asin,head_csv,d_csv,proxy,headers,t)
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
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'cookie':r'session-id=134-2268601-6510461; ubid-main=130-7632543-3841849; aws-ubid-main=618-6315556-8710572; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A200473898053%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22keto1%22%2C%22keybase%22%3A%22By10goehxkEz1G5fdXRSY%2BsAg%2BZYNjgG%2F3%2BEM4LABIg%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; session-token=rjpFr7RTZ9j61eUOxcXQy3OALjfXxGfpsKtXkwwatALp/UMc+Rr6L+8fZKcCkZYyjkanoWo2JgxYiHDQ1y0kql4YydqPdfoxzRDmVPx5n9he9KvEo+/+JRYs1TUSDcA3BaVVX+QeE76xQDPQoZdNYqaa77KMgRgfLuWU5gZfSZScyWiXD60pQLsLf5DraIuo'
            }
    username = '代理账号'
    password = '代理密码'
    PROXY_RACK_DNS = '代理地址'
    proxy = {"https": "http://{}:{}@{}".format(username, password, PROXY_RACK_DNS)}

    #相关设置
    url=url
    csv_path="./pro/{ite}.csv".format(ite=ite) #用来存放采集到的数据
    asin_path="./asin/{ite}.txt".format(ite=ite)#可不修改，用来临时存放asin
    
    #新建或者清空asin文件
    open(asin_path,"w",encoding="utf8",newline="") 
    #采集asin
    for i in find_x():
        if m_page == -1:
            pass
        elif i > m_page:
            print('采集完{i}页的asin'.format(i=i))
            break
        else:
            pass
        try:
            #获取下一页url和本页面的产品url
            bs=find_bs(url,headers,proxy)
            print('成功获取bs')
            page_url,asins=find_page_url(bs,asin_path)
            print('成功获取产品asin和下一页')
            str_asins="".join(asins)
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

    with open(asin_path,'r',encoding='utf8') as f:
        q_asin_list=set()
        all_asin=[]
        q_asins=Manager().Queue()
        q = Manager().Queue()
        q_asin=Manager().Queue()
        for asin in f:
            t=5
            main_asin=re.sub("\n",'',asin)
            try:
                find_pro(csv_path,main_asin,proxy,headers,head_csv,t,q_asin,q_asin_list,q,q_asins,all_asin,max_asin)
                print('采集完{asin}'.format(asin=main_asin))
            except Exception as e:
                print('采集{asin}失败,跳过'.format(asin=main_asin),e)
                while q.empty()==False:
                    q.get()
                print('成功清空q')

if __name__ =="__main__":
    m_page=1 #采集最大页数 -1为全部
    max_asin=5 #采集变体最大数 -1为全部
    with open('./urls','r',encoding='utf-8') as f: #urls存放要采集的亚马逊搜索列表
        readCSV=csv.reader(f)
        for row in readCSV:
            ite=row[0].title().replace(" ", "")
            if '#' in ite:
                print('跳过{ite}'.format(ite=ite))
                continue
            url=row[1]
            find_pro_ite(ite,url,m_page,max_asin)
