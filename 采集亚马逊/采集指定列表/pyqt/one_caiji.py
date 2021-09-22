#-*-coding:utf-8 -*-
#解决无法采集下拉形式的尺寸变量名问题
#
from os import path, write
from typing import Text
from selenium import webdriver
import datetime
import time
import csv
import lxml
from lxml import etree
import re
import os
from set import cread_ini,read_ini
from selenium.webdriver.chrome import options

def find_driver():
    prefs = {"profile.managed_default_content_settings.images": 2}  #设置无图模式
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--lang=en")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches",["enable-logging"])
    options.add_argument('ignore-certificate-errors')

    driver=webdriver.Chrome(options=options,executable_path=find_path()[0])
    return driver

#获取html
def find_html(url,page):
    print("请求{url}".format(url=url))
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    driver=find_driver()
    driver.get(url)
    #调出输入框
    try:
        button1=driver.find_element_by_xpath("//*[@id='glow-ingress-block']")
    except Exception as e:
        print("查找邮编输入:",e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url,page)

    button1.click()

    #输入邮编
    wait = WebDriverWait(driver, 10, 0.5)
    element = wait.until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))#等待
    element.send_keys("10041")
    #点击发送
    button2=driver.find_element_by_xpath("//*[@id='GLUXZipUpdate']/span/input")
    WebDriverWait(driver,10,0.2).until(lambda driver:button2.is_displayed())#显式等待
    button2.click()
    time.sleep(0.5)
    print("一次刷新")
    driver.refresh()
    try:
        driver.implicitly_wait(30)
        driver.set_script_timeout(30)
        driver.set_page_load_timeout(30)
    except Exception as e:
        print("超时:",e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url,page)

    a=0
    while a<1:
        try:
            print("下拉",a)
            a=a+1
            
            driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*1/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*2/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*3/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*4/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            
            
            #上拉到顶部
            print("上拉")
            driver.execute_script("window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*4/5); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            
        except Exception as e:
            print("拉动:",e)
            print("开始关闭浏览器")
            driver.close()
            driver.quit()
            print("成功关闭浏览器")
            return find_html(url,page)
        ''''''
        if page=="ok":
            print("采集列表")
            #wait = WebDriverWait(driver, 10, 0.5)
            #element = wait.until(EC.presence_of_element_located((By.ID, "search")))
            #element.send_keys("selenium")
        ''''''
    #print("二次刷新")
    #driver.refresh()
    try:
        driver.implicitly_wait(5)
        driver.set_script_timeout(5)
        driver.set_page_load_timeout(5)
    except Exception as e:
        print("超时:",e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url,page)
    try:
        html=driver.page_source
    except Exception as e:
        print("获取html:",e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url,page)

    print("html=",len(html))
    print("开始关闭浏览器")
    driver.close()
    driver.quit()
    print("成功关闭浏览器")
    html2=etree.HTML(html)
    return html,html2

#获取品牌
def find_brand(html1,html2):
    html1=html1
    brand=html2.xpath("//*[@id='bylineInfo']/text()")
    try:
        brand=brand[0]
        brand=re.sub("Visit the|Store|Brand|:","",brand)
        brand=brand.strip()
        brand=brand.title()
    except Exception as e:
        print("获取品牌",e)
        brand=""
    return brand

def find_stock(html1,html2):
    #获取库存
    stock =html2.xpath("//*[@id='availability']/span/text()")
    try:
        stock =stock [0]
        stock =stock .strip()
        print("库存信息：",stock)
        if "Usually ships soon.".lower() in stock.lower():
            print(" Usually ships soon. 没库存")
            stock=0
            return stock
        if "Temporarily out of stock.".lower() in stock.lower():
            print("Temporarily out of stock. 没库存")
            stock=0
            return stock
        if "In stock soon.".lower() in stock.lower():
            print("In stock soon 没库存")
            stock=0
            return stock
        if "ships within" in stock.lower():
            print("ships within 木有库存")
            stock=0
            return stock
        if "Currently unavailable".lower() in stock.lower():
            stock=0
            return stock
        if stock.lower()=="In Stock.".lower():
            print("库存充足")
            return 100
        mo=re.compile("[0-9]+")
        stock=mo.findall(stock)
        if stock==[]:
            stock=100
            print("库存充足")
        stock=stock[0].strip()
        stock=int(stock)
        print("库存:",stock)
        return stock
    except Exception as e:
        print("获取库存:",e)
        stock =100
    return stock 

#获取卖家名
def find_fromShips(html1,html2):
    html1=html1
    #fromships=html2.xpath("normalize-space(//*[@id='tabular-buybox-truncate-0']/span[2]/span/text()|//*[@id='SSOFpopoverLink']/text()|string(//div[@id='merchant-info']))")
    r = html2.xpath("//*[@id='tabular-buybox-truncate-0']/span[2]/span/text()")
    r = r or html2.xpath("normalize-space(string(//div[@id='merchant-info']))")
    r = r or html2.xpath("//*[@id='SSOFpopoverLink']/text()")
    if isinstance(r, list) and len(r) > 0:
        r = r[0]
    print("卖家信息",r)
    fromship=r
    return fromship

def find_title(html1,html2):
    html1=html1
    #获取标题
    title=html2.xpath("//*[@id='productTitle']")
    try:
        title=title[0].text
        title=title.strip()
        title=title.title()
    except Exception as e:
        print(e)
        title=""
    return title

def find_price(html1,html2):
    html1=html1
    #获取价格
    prices=html2.xpath("//*[@id='priceblock_ourprice']/text()|//*[@id='priceblock_saleprice']/text()|//*[@id='color_name_0_price']/p/text()|//*[@id='price']/table/tbody/tr[1]/td[2]/span[1]/text()")
    price=""
    try:
        price=prices[0]
    except Exception as e:
        print(e)
    return price

def find_asins1(html1,html2):
    html1=html1
    #获取所有变体
    asins=html2.xpath("//*/ul/li/@data-defaultasin")
    asins=list(set(asins))
    return asins

def find_asins(html1,html2):
    mo=re.compile("asinVariationValues.+")
    datas=mo.findall(html1)
    mo2=re.compile("[A-Z0-9]{10}")
    asins=mo2.findall(datas[0])
    asins=list(set(asins))
    return asins

def find_colour(html1,html2):
    html1=html1
    #获取颜色
    colours=html2.xpath("//*[@id='variation_color_name']/div/span/text()")
    colour=""
    try:
        colour=colours[0]
    except Exception as e:
        print(e)
    return colour

def find_style(html1,html2):
    html1=html1
    #获取样式
    styles=html2.xpath("//*[@id='variation_style_name']/div/span/text()")
    style=""
    try:
        style=styles[0]
    except Exception as e:
        print(e)
    return style

def find_var_size(html1,html2):
    html1=html1
    #获取变体尺寸
    sizes=html2.xpath("//*[@id='variation_size_name']/div/span/text()")
    size=""
    try:
        size=sizes[0]
    except Exception as e:
        print(e)
    if size=="":
        sizes2=html2.xpath("//*[@id='dropdown_selected_size_name']/span/span/span/text()")
        try:
            size=sizes2[0]
        except Exception as e:
            print(e)
    return size.strip()

def find_size(html1,html2):
    html1=html1
    #获取商品尺寸
    sizes=html2.xpath("//*[@id='productOverview_feature_div']/div/table/tbody/tr[*]/td[*]/span/text()")
    ok=False
    size=""
    for i in sizes:
        if ok:
            size=i.strip()
            break
        if i.title()=="Size":
            ok=True
    return size

def find_count(html1,html2):
    html1=html1
    #获取每包数量变量
    counts=html2.xpath("//*[@id='variation_configuration']/div/span/text()")
    count=""
    try:
        count=counts[0]
    except Exception as e:
        print(e)
    return count

def find_Package_size(html1,html2):
    html1=html1
    #获取包装尺寸
    pg_sizes_name=html2.xpath("//*[@id='productDetails_techSpec_section_1']/tbody/tr[*]/th/text()")
    pg_sizes_value=html2.xpath("//*[@id='productDetails_techSpec_section_1']/tbody/tr[*]/td/text()")
    pg_size=""
    for i in range(len(pg_sizes_name)):
        if pg_sizes_name[i].strip()=="Package Dimensions":
            pg_size=pg_sizes_value[i]
    if pg_size=="":
        #采用正则方式获取
        mo=re.compile("^[0-9]+(\.?[0-9]+)?$\s+x\s+^[0-9]+(\.?[0-9]+)?$\s+x\s+^[0-9]+(\.?[0-9]+)?$")
        pg=mo.findall(html1)
        for i in range(len(pg)):
            pg_size=pg[i].strip()
    return pg_size

def find_LxWxH(html1,html2):
    html1=html1
    #获取尺寸
    mate_name=html2.xpath("//*[@id='productOverview_feature_div']/div/table/tbody/tr[*]/td[*]/span|//*[@id='poExpander']/div[*]/div/table/tbody/tr[*]/td[*]/span")
    ok=False
    LxWxH=""
    for i in mate_name:
        if ok:
            LxWxH=i.text
            break
        #获取包装尺寸
        if i.text=="Item Dimensions LxWxH":
            ok=True
    return LxWxH

def to_lwh(html1):
    mo=re.compile("(\d+)(\.\d+)?")
    mo2=re.compile("[a-zA-Z]{2,100}")
    pg=mo.findall(html1)
    co=mo2.findall(html1)

    l="".join(pg[0])
    w="".join(pg[1])
    h="".join(pg[2])

    lwh="{l},{w},{h},{c}".format(c=co[0],l=l,w=w,h=h)
    return lwh

def find_material(html1,html2):
    html1=html1
    #获取材料
    mate_name=html2.xpath("//*[@id='productOverview_feature_div']/div/table/tbody/tr[*]/td[*]/span|//*[@id='poExpander']/div[*]/div/table/tbody/tr[*]/td[*]/span")
    ok=False
    material=""
    for i in mate_name:
        if ok:
            material=i.text
            break
        #如果当前是Material，紧接的就是材料值
        if i.text=="Material":
            ok=True
    return material

def find_Fabric_Type(html1,html2):
    html1=html1
    #织物类型
    fabric_type=html2.xpath("//*[@id='productOverview_feature_div']/div/table/tbody/tr[*]/td[*]/span|//*[@id='poExpander']/div[*]/div/table/tbody/tr[*]/td[*]/span")
    ok=False
    fabrictype=""
    for i in fabric_type:
        if ok:
            fabrictype=i.text
            break
        if i.text.strip()=="Fabric Type":
            ok=True
    return fabrictype


def find_pattern(html1,html2):
    html1=html1
    #获取图案
    patterns=html2.xpath("//*[@id='productOverview_feature_div']/div/table/tbody/tr[*]/td[*]/span|//*[@id='poExpander']/div[*]/div/table/tbody/tr[*]/td[*]/span")
    ok=False
    pattern=""
    for i in patterns:
        if ok:
            pattern=i.text
            break
        if i.text=="Pattern" or i.text=="pattern":
            ok=True
    return pattern


def find_weight(html1,html2):
    html1=html1
    import re
    #获取重量
    weight_name=html2.xpath("//*[@id='productDetails_detailBullets_sections1']/tbody/tr[*]/th/text()|//*[@id='productDetails_techSpec_section_1']/tbody/tr[*]/th/text()")
    weight_value=html2.xpath("//*[@id='productDetails_detailBullets_sections1']/tbody/tr[*]/td/text()|//*[@id='productDetails_techSpec_section_1']/tbody/tr[*]/td/text()")
    weight=""
    for i in range(len(weight_name)):
        if weight_name[i].strip()=="Item Weight":
            weight=weight_value[i]
    w=weight.strip()
    if w=="":
        mo=re.compile("\d{0,5}\.\d{0,5}.{1,3}Ounces|\d{0,5}\.\d{0,5}.{1,3}ounces|\d{0,5}\.\d{0,5}.{1,3}Pounds|\d{0,5}\.\d{0,5}.{1,3}pounds|\d{0,5}\.\d{0,5}.{1,3}lbs|\d{0,5}\.\d{0,5}.{1,3}Lbs|\d{0,5}\.\d{0,5}\s+OZ|\d{0,5}\.\d{0,5}\s+Oz|\d{0,5}\.\d{0,5}\s+oz")
        weights=mo.findall(html1)
        for i in range(len(weights)):
            w=weights[i].strip()
    return w
def find_des(html1,html2):
    html1=html1
    #获取描述
    des=html2.xpath("//*[@id='feature-bullets']/ul/li[*]/span/text()")
    dess=[]
    for d in des:
       d=d.strip()
       if d!="":
            dess.append(d+r"\n")
    return dess

def find_imges(html1,html2):
    html1=html1
    imges=html2.xpath("//*[@id='altImages']/ul/li/span/span/span/span/img/@src")
    pics=[]
    try:
        for i in imges:
            pic=re.sub("_.{0,1000}_\\.","",i)
            pics.append(pic)
    except Exception as e:
        print(e)
    return pics

def find_pro_n(home_asin,all_asin):
    import csv
    url="https://www.amazon.com/dp/"+home_asin
    html1,html2=find_html(url,page="")
    try:
        asins=find_asins(html1,html2)
    except Exception as e:
        print("没获取到变体,认为该商品木有变体",e)
        asins=[]
    
    if asins==[]:
        asins.append(home_asin)
    n=0
    datas=[]
    b=0
    for asin in asins:
        print("所有变体：",asins)
        print("采集变体",asin)
        if b>15 and len(asins)>3:
            break
        n=n+1
        if asin=="":
            continue
        url="https://www.amazon.com/dp/"+asin
        a=0
        nature=[] #属性列表 当采集到的属性很多 而个别属性拿不到时 判断该产品就是木有这个属性
        while len(nature)<2:
            a=a+1
            b=b+1
            if a>10:
                break
            print("请求:",a,"次",url)
            html1,html2=find_html(url,page="")
            #通过价格形式判断是否在url后面增加 ?th=1&psc=1
            price=find_price(html1,html2)
            if "-" in price:
                #如果价格中包括"-"，就在URL后面加?th=1&psc=1重写请求
                url=url+r"?th=1&psc=1"
                html1,html2=find_html(url,page="")
            fromship=find_fromShips(html1,html2)
            print("卖家:",fromship)
            stock=find_stock(html1,html2)
            print("库存为：",stock)
            if fromship=="" or "mazon" not in fromship:
                print("卖家不是 Amazon 跳过")
                break
            '''判断是否跳过代码结束'''
            print("品牌:",find_brand(html1,html2))
            brand=find_brand(html1,html2)
            if brand=="":
                continue
            nature.append(brand) #品牌写入
            print("标题:",find_title(html1,html2))
            title=find_title(html1,html2)
            title=re.sub(brand,"",title)
            if title=="":
                continue
            nature.append(title)#标题写入
            print("价格:",find_price(html1,html2))
            price=find_price(html1,html2)
            if price=="":
                continue
            nature.append(price) #价格写入

            material=find_material(html1,html2)
            print("材料:",material)
            
            var_color=find_colour(html1,html2)
            print("颜色变量:",var_color)

            var_style=find_style(html1,html2)
            print("样式变量:",var_style)

            var_size=find_var_size(html1,html2)
            print("变量尺寸:",var_size)
            count=find_count(html1,html2)
            print("件数变量:",count)

            size=find_size(html1,html2)
            print("商品尺寸:",size)

            pk_size=find_Package_size(html1,html2)
            if pk_size=="":
                pk_size=find_LxWxH(html1,html2)
            try:
                pk_size=to_lwh(pk_size)
            except Exception as e:
                print(e)
                pk_size=""

            print("包装尺寸:",pk_size)
            
            Pattern=find_pattern(html1,html2)
            print("图案:",Pattern)
            Fabric_Type=find_Fabric_Type(html1,html2)
            print("织物类型:",Fabric_Type)

            
            weight=find_weight(html1,html2)
            print("重量:",weight)
            
            desc=find_des(html1,html2)
            desc="\n".join(desc)
            print("描述:",desc)

            nature.append(desc) #描述写入
            print("图片:",find_imges(html1,html2))
            imges=find_imges(html1,html2)
            if imges=="":
                continue
            nature.append(imges)#图片写入
            parent=""
            types="simple"
            data=[types,asin,title,price,weight,desc,var_color,var_style,count,var_size,Pattern,material,size,pk_size,Fabric_Type,",".join(imges),parent]
            datas.append(data)
            all_asin.append(asin)
            break
    n=0
    index_asin=""
    if len(datas)==0:
        pass
    for data in datas:
        with open(find_path()[2],"a",newline="",encoding="utf-8-sig") as f:
            wt=csv.writer(f)
            if len(datas)==1:
                data[0]="simple"
            elif len(datas)>1 and n==0:
                data[0]="variable"
                index_asin=data[1]
            else:
                data[0]="variation"
                data[16]=index_asin
            wt.writerow(data)
            print("成功写入:",data[1])
        n=n+1

def find_asins_nextpage(url):
    n=0
    while True:
        n=n+1
        print("n=",n)
        if n>10:
            next_page=""
            break
        try:
            print("开始请求：",url)
            page="ok"
            _,html2=find_html(url,page)
        except Exception as e:
            print("获取html",e)
            next_page=""
            time.sleep(1)
            continue
        
        xp_asins=html2.xpath("//*/div/@data-asin")
        asins=[]
        for i in xp_asins:
            if len(i)>3:
                asins.append(i)
        xp_page=html2.xpath("//*[@class='s-pagination-strip']/a/@href")
        if xp_page==[]:
            xp_page=html2.xpath("//*[@class='a-last']/a/@href")
        print("xp_page:",xp_page)
        try:
            next_page="https://www.amazon.com"+xp_page[-1]
            print("nextupl:",next_page)
            if len(next_page)>0:
                print("成功采集下一页")
                break
        except Exception as e:
            print("e")
            next_page=""
    return asins,next_page

def wt_csv(d_csv,csv_path):
    with open(csv_path,"a",encoding='utf8',newline='') as f:
        f_csv=csv.DictWriter(f,head_csv)
        for i in d_csv:
            f_csv.writerow(i)
    print('成功写入')

def find_path():
    #设置文件保存路径
    #读取配置文件，从配置文件获取保存路径
    ini_path=r"./seting.ini"
    data=read_ini(ini_path)
    #path=r"F:\py\谷歌站长平台\批量操作\采集亚马逊_纯粹采集\hot\hot0922.csv"
    return data

def wt_head_csv(head_csv):
    with open(find_path()[2],"w",newline="",encoding="utf-8-sig") as f:
        wt=csv.writer(f)
        wt.writerow(head_csv)
        print("成功写入表头:",head_csv)

if __name__=="__main__":
    head_csv=["types","asin","title","price","weight","desc","var_colour","var_style","count","var_size","Pattern","material","size","pk_size","Fabric Type","imges","Parent"]
    if os.path.exists(find_path()[2])==False:
        wt_head_csv(head_csv)
    
    mo=re.compile("dp/[0-9A-Z]{10}")
    all_asin=[]

    with open(find_path()[1],"r") as f1:
        datas=f1.readlines()
        for i in datas:
            if r"#" in i:
                print("跳过{}".format(i))
                continue
            asins=mo.findall(i)
            if len(asins)>0:
                for asin in asins:
                    #print(asin[3:])
                    all_asin.append(asin[3:])
    print(all_asin)
    asins=list(set(all_asin))
    all_asin=[]
    for asin in asins:
        if asin in []:
            continue
        #开始采集一个产品
        try:
            if asin in all_asin:
                print("{asin}已采集过，跳过".format(asin=asin))
                continue
            find_pro_n(asin,all_asin)
            print("采集完所有变体:",asin)
        except Exception as e:
            print("采集",asin,"失败",e)
