#-*-coding:utf-8 -*-
#from _typeshed import IdentityFunction
from os import path, write
from typing import Text
from selenium import webdriver
import datetime
import time,bs4
import csv
import lxml
from lxml import etree
import re
#获取html
def find_html(url):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    driver=find_driver()
    driver.get(url)
    time.sleep(0)
    driver.implicitly_wait(30)
    
    a=0
    while a<3:
        print("下拉",a)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        a=a+1
        time.sleep(0.5)
        '''
        wait = WebDriverWait(driver, 10, 0.5)
        element = wait.until(EC.presence_of_element_located((By.ID, "MAIN-PAGINATION-33")))
        element.send_keys("selenium")
        '''
    time.sleep(0)
    html=driver.page_source
    driver.get_cookies()
    driver.close()
    driver.quit()
    print("html=",len(html))
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
    except Exception as e:
        print("获取品牌",e)
        brand=""
    return brand

def find_title(html1,html2):
    html1=html1
    #获取标题
    title=html2.xpath("//*[@id='productTitle']")
    try:
        title=title[0].text
        title=title.strip()
    except Exception as e:
        print(e)
        title=""
    return title

def find_price(html1,html2):
    html1=html1
    #获取价格
    prices=html2.xpath("//*[@id='priceblock_ourprice']/text()|//*[@id='priceblock_saleprice']/text()|//*[@id='color_name_0_price']/p/text()")
    price=""
    try:
        price=prices[0]
    except Exception as e:
        print(e)
    return price

def find_asins(html1,html2):
    html1=html1
    #获取所有变体
    asins=html2.xpath("//*/ul/li/@data-defaultasin")
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

def find_size(html1,html2):
    html1=html1
    #获取尺寸
    sizes=html2.xpath("//*[@id='variation_size_name']/div/span/text()")
    size=""
    try:
        size=sizes[0]
    except Exception as e:
        print(e)
    return size

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

def find_Package_size(html1,html2):
    html1=html1
    #获取包装尺寸
    pg_sizes_name=html2.xpath("//*[@id='productDetails_techSpec_section_1']/tbody/tr[*]/th/text()")
    pg_sizes_value=html2.xpath("//*[@id='productDetails_techSpec_section_1']/tbody/tr[*]/td/text()")
    pg_size=""
    for i in range(len(pg_sizes_name)):
        if pg_sizes_name[i].strip()=="Package Dimensions":
            pg_size=pg_sizes_value[i]
    return pg_size


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
        #mo=re.compile("\d{0,5}\.\d{0,5}.{1,3}Ounces|\d{0,5}\.\d{0,5}.{1,3}ounces|\d{0,5}\.\d{0,5}.{1,3}Pounds|\d{0,5}\.\d{0,5}.{1,3}pounds|\d{0,5}\.\d{0,5}.{1,3}lbs|\d{0,5}\.\d{0,5}.{1,3}Lbs")
        mo=re.compile("\d{0,5}.\d{0,5}.{1,3}Ounces|\d{0,5}.\d{0,5}.{1,3}ounces|\d{0,5}.\d{0,5}.{1,3}Pounds|\d{0,5}.\d{0,5}.{1,3}pounds|\d{0,5}.\d{0,5}.{1,3}lbs|\d{0,5}.\d{0,5}.{1,3}Lbs")
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

def find_pro_n(home_asin):
    import csv
    url="https://www.amazon.com/dp/"+home_asin
    html1,html2=find_html(url)
    
    asins=find_asins(html1,html2)
    n=0
    while len(asins)==0:
        n=n+1
        print("查找变体：",n)
        html1,html2=find_html(url)
        
        asins=find_asins(html1,html2)
        if n>5:
            break
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
        while True:
            a=a+1
            b=b+1
            if a>10:
                break
            print("请求:",a,"次",url)
            html1,html2=find_html(url)
            
            print("品牌:",find_brand(html1,html2))
            brand=find_brand(html1,html2)
            if brand=="":
                continue
            print("标题:",find_title(html1,html2))
            title=find_title(html1,html2)
            title=re.sub(brand,"",title)
            if title=="":
                continue
            print("价格:",find_price(html1,html2))
            price=find_price(html1,html2)
            if price=="":
                continue
            print("材料:",find_material(html1,html2))
            material=find_material(html1,html2)
            print("颜色:",find_colour(html1,html2))
            color=find_colour(html1,html2)
            print("尺寸:",find_size(html1,html2))
            size=find_size(html1,html2)
            print("包装尺寸:",find_Package_size(html1,html2))
            pk_size=find_Package_size(html1,html2)
            print("重量:",find_weight(html1,html2))
            weight=find_weight(html1,html2)
            print("描述:",find_des(html1,html2))
            desc=find_des(html1,html2)
            desc="\n".join(desc)
            print("图片:",find_imges(html1,html2))
            imges=find_imges(html1,html2)
            if imges=="":
                continue
            parent=""
            types="simple"
            Pattern=find_pattern(html1,html2)
            print("图案:",Pattern)
            Fabric_Type=find_Fabric_Type(html1,html2)
            print("织物类型:",Fabric_Type)
            data=[types,asin,title,price,weight,desc,color,Pattern,material,size,pk_size,Fabric_Type,",".join(imges),parent]
            datas.append(data)
            break
    n=0
    index_asin=""
    if len(datas)==0:
        pass
    for data in datas:
        with open(find_path(),"a",newline="",encoding="utf-8-sig") as f:
            wt=csv.writer(f)
            if len(datas)==1:
                data[0]="simple"
            elif len(datas)>1 and n==0:
                data[0]="variable"
                index_asin=data[1]
            else:
                data[0]="variation"
                data[13]=index_asin
            wt.writerow(data)
            print("成功写入:",data[1])
        n=n+1


def find_driver():
    #prefs = {"profile.managed_default_content_settings.images": 2}  #设置无图模式
    options = webdriver.ChromeOptions()
    #options.add_experimental_option("prefs", prefs)
    options.add_argument("--lang=en")
    options.add_argument("--headless")
    #driver=webdriver.Chrome(options=options,executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    driver=webdriver.Chrome(options=options,executable_path=r"/Users/gaotiansong/Downloads/chromedriver")
    return driver

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
            _,html2=find_html(url)
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
    path=r"./exercise_mat.csv"
    return path

if __name__=='__main__':
    import re
    #driver=webdriver.Chrome(executable_path=r'/Users/gaotiansong/Public/chromedriver')
    #文件保存路径
    url="https://www.amazon.com/s?k=exercise+mat&i=sporting&rh=n%3A3375251%2Cp_76%3A1249176011%2Cp_72%3A1248957011%2Cp_n_condition-type%3A6503254011&dc&qid=1629168438&rnid=6503252011&ref=sr_nr_p_n_condition-type_1"
    head_csv=["types","asin","title","price","weight","desc","colour","Pattern","material","size","pk_size","Fabric Type","imges","Parent"]
    with open(find_path(),"w",newline="",encoding="utf-8-sig") as f:
        wt=csv.writer(f)
        wt.writerow(head_csv)
        print("成功写入表头:",head_csv)
    ls_page=[]
    pg=[]
    while True:
        if pg not in ls_page:
            ls_page.append(pg)
        else:
            print("全部采集完毕")
            break
        print("ls_page:",ls_page)
        asins,nextpage=find_asins_nextpage(url)
        print("asins:",asins)
        for asin in asins:
            if asin in []:
                continue
            #开始采集一个产品
            try:
                find_pro_n(asin)
                print("采集完所有变体:",asin)
            except Exception as e:
                print("采集",asin,"失败",e)
        url=nextpage
        #提取表示页数的 page=2 
        mo=re.compile("page=[0-9]{0,100}")
        pg=mo.findall(url)
