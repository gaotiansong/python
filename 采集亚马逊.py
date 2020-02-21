#-*- coding：utf-8 -*-
import requests,bs4,re,time,csv,os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def find_bs(url,driver_path):
    opt = webdriver.ChromeOptions()
    #opt.add_argument("--headless") #新版本设置无头
    opt.add_argument("--disable-gpu")
    opt.add_argument('lang=en-us.UTF-8')
    #driver = webdriver.Chrome(executable_path='/Users/gaotiansong/Downloads/chromedriver',options=opt) #驱动器路径
    driver = webdriver.Chrome(executable_path=driver_path,options=opt) #驱动器路径
    m=0
    while m<3:
        try:
            driver.get(url)
            driver.set_page_load_timeout(30)
            a=0
            while a<1:
                #下拉鼠标
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                time.sleep(5)
                a=a+1
            break
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'链接失败,重试',m,'次')
            html=''
            print('抓取hmtl失败，重新拨号')
            driver.get_cookies()
            driver.quit()
            reconnect_ADSL()#重连ADSL
        m=m+1

    html=driver.page_source
    driver.get_cookies()
    driver.quit()
    bs=bs4.BeautifulSoup(html,'html.parser')
    return bs

def pro_ls(bs):
    #得出h2中的a标签，及链接
    ls_bs=bs.select('h2 a')
    if ls_bs==[]:
        reconnect_ADSL()#重连ADSL
        find_bs(url,driver_path)
    else:
        pass
    
    ls=[]
    for l in ls_bs:
        #得出字符串形式的链接
        l='https://www.amazon.com'+l.get('href')
        #过滤链接
        if 'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref' in l:
            continue
        else:
            pass
        #删除链接中的多余字符
        l=re.sub('\=.*','',l)
        ls.append(l)
    return ls

#得出商品标题
def find_title(bs):
    title=bs.select('h1')
    try:
        title=title[0].getText()
        title=re.sub('\/|\.|\n|\(.*\)|,|\|','',title)
        title=title.strip()#去除首位空格
    except:
        print('获取h1失败')
        title=''
    return title
#得出商品url
def find_handle(title):
    handle=re.sub(' ','-',title)
    return handle
#采集描述
def find_body(bs):
    bodys=bs.select('#feature-bullets')
    s=''
    for b in bodys:
        body=b.getText()
        body=body.strip()#去除收尾空格
        body=re.sub('	|\n','',body)
        s=s+body
    return s
    
#得出商品图片
def find_imgs(bs):
    try:
        imgs_ls=bs.select('span .a-button-inner img')
        imgs=[]
        n=1
        for img in imgs_ls:
            img=img.get('src')
            #if '.png' in img:
            if ('.png' in img)or('gif'in img):
                continue
            else:
                pass
            img=re.sub('\._.*\.jpg','.jpg',img)
            imgs.append(img)
            n=n+1
    except:
        imgs=[]
        print('没找到图片')
    return imgs

def find_price(bs):
    p=bs.select('#price_inside_buybox')
    try:
        p=p[0].getText()
        p=p.strip()#去除首位空格
        p=re.sub('\$','',p)
    except:
        p='0'
    return p

def wt_to_csv(file,path_csv):
    csvFile=open(path_csv,'a',encoding='utf-8',newline='')
    writer=csv.writer(csvFile)#初始化表格
    try:
        writer.writerow(file)#写入内容
    except:
        print('写入内容失败，跳过')
    csvFile.close()

def f_head():
    #设置表头
    a1='Handle'
    b1='Title'
    c1='Body (HTML)'
    d1='Vendor'
    e1='Type'
    f1='Tags'
    g1='Published'
    h1='Option1 Name'
    i1='Option1 Value'
    j1='Option2 Name'
    k1='Option2 Value'
    l1='Option3 Name'
    m1='Option3 Value'
    n1='Variant SKU'
    o1='Variant Grams'
    p1='Variant Inventory Tracker'
    q1='Variant Inventory Qty'
    r1='Variant Inventory Policy'
    s1='Variant Fulfillment Service'
    t1='Variant Price'
    u1='Variant Compare At Price'
    v1='Variant Requires Shipping'
    w1='Variant Taxable'
    x1='Variant Barcode'
    y1='Image Src'
    z1='Image Position'
    aa1='Image Alt Text'
    ab1='Gift Card'
    ac1='SEO Title'
    ad1='SEO Description'
    ae1='Google Shopping / Google Product Category'
    af1='Google Shopping / Gender'
    ag1='Google Shopping / Age Group'
    ah1='Google Shopping / MPN'
    ai1='Google Shopping / AdWords Grouping'
    aj1='Google Shopping / AdWords Labels'
    ak1='Google Shopping / Condition'
    al1='Google Shopping / Custom Product'
    am1='Google Shopping / Custom Label 0'
    an1='Google Shopping / Custom Label 1'
    ao1='Google Shopping / Custom Label 2'
    ap1='Google Shopping / Custom Label 3'
    aq1='Google Shopping / Custom Label 4'
    ar1='Variant Image'
    as1='Variant Weight Unit'
    at1='Variant Tax Code'
    au1='Cost per item'
    filehead=[a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1,u1,v1,w1,x1,y1,z1,aa1,ab1,ac1,ad1,ae1,af1,aj1,ah1,ai1,aj1,ak1,al1,am1,an1,ao1,ap1,aq1,ar1,as1,at1,au1]
    return filehead

#采集单条内容的方法
def caiji_shopify(url):
    bs=find_bs(url,driver_path)
    title=find_title(bs)
    handle=find_handle(title)
    body=find_body(bs)
    imgs=find_imgs(bs)
    p=find_price(bs)
    a0=handle#Handle
    b0=title#'Title'
    c0=body#'Body (HTML)'
    d0='customadd'#'Vendor'
    e0='hat'#'Type'
    f0='hat,custom hat,hats'#'Tags'
    g0='TRUE'#'Published'
    h0=title#'Option1 Name'
    i0=title#'Option1 Value'
    j0=''#'Option2 Name'
    k0=''#'Option2 Value'
    l0=''#'Option3 Name'
    m0=''#'Option3 Value'
    n0=''#'Variant SKU'
    o0='0'#'Variant Grams'
    p0=''#'Variant Inventory Tracker'
    q0='0'#'Variant Inventory Qty'
    r0='continue'#'Variant Inventory Policy'
    s0='manual'#'Variant Fulfillment Service'
    t0=p#'Variant Price'
    u0=p#'Variant Compare At Price'
    v0='TRUE'#'Variant Requires Shipping'
    w0='FALSE'#'Variant Taxable'
    x0=''#'Variant Barcode'
    try:
        y0=imgs[0]#'Image Src'图片地址
    except:
        y0=''
    z0='1'#'Image Position'图片位置
    aa0=title#'Image Alt Text'
    ab0='FALSE'#'Gift Card'
    ac0=''#'SEO Title'
    ad0=''#'SEO Description'
    ae0=''#'Google Shopping / Google Product Category'
    af0=''#'Google Shopping / Gender'
    ag0=''#'Google Shopping / Age Group'
    ah0=''#'Google Shopping / MPN'
    ai0=''#'Google Shopping / AdWords Grouping'
    aj0=''#'Google Shopping / AdWords Labels'
    ak0=''#'Google Shopping / Condition'
    al0=''#'Google Shopping / Custom Product'
    am0=''#'Google Shopping / Custom Label 0'
    an0=''#'Google Shopping / Custom Label 1'
    ao0=''#'Google Shopping / Custom Label 2'
    ap0=''#'Google Shopping / Custom Label 3'
    aq0=''#'Google Shopping / Custom Label 4'
    ar0=''#'Variant Image'
    as0='kg'#'Variant Weight Unit'
    at0=''#'Variant Tax Code'
    au0=''#'Cost per item'
    f0_csv=[a0,b0,c0,d0,e0,f0,g0,h0,i0,j0,k0,l0,m0,n0,o0,p0,q0,r0,s0,t0,u0,v0,w0,x0,y0,z0,aa0,ab0,ac0,ad0,ae0,af0,aj0,ah0,ai0,aj0,ak0,al0,am0,an0,ao0,ap0,aq0,ar0,as0,at0,au0]

    #如果表格为空，则写入表头
    size=os.path.getsize(path_csv)
    if size==0:
        filehead=f_head()
        wt_to_csv(filehead,path_csv)
    else:
        pass

    if len(imgs)>1:
        n=1
        for img in imgs:
            if n==1:
                e0='【商品分类】' #分类
                f0='【商品tag】' #tag
                y0=img
                z0=str(n)
                #设置seo标题
                ac0='【seo标题】'+' '+title
                f0_csv=[a0,b0,c0,d0,e0,f0,g0,h0,i0,j0,k0,l0,m0,n0,o0,p0,q0,r0,s0,t0,u0,v0,w0,x0,y0,z0,aa0,ab0,ac0,ad0,ae0,af0,aj0,ah0,ai0,aj0,ak0,al0,am0,an0,ao0,ap0,aq0,ar0,as0,at0,au0]
                wt_to_csv(f0_csv,path_csv)
            else:
                a0=handle
                b0=''
                c0=''
                d0=''
                e0=''
                f0=''
                g0=''
                h0=''
                i0=''
                j0=''
                k0=''
                l0=''
                m0=''
                n0=''
                o0=''
                p0=''
                q0=''
                r0=''
                s0=''
                t0=''
                u0=''
                v0=''
                w0=''
                x0=''
                y0=''
                z0=''
                aa0=''
                ab0=''
                ac0=''
                ad0=''
                ae0=''
                af0=''
                ag0=''
                ah0=''
                ai0=''
                aj0=''
                ak0=''
                al0=''
                am0=''
                an0=''
                ao0=''
                ap0=''
                aq0=''
                ar0=''
                as0=''
                at0=''
                au0=''
                y0=img
                z0=str(n)
                f0_csv=[a0,b0,c0,d0,e0,f0,g0,h0,i0,j0,k0,l0,m0,n0,o0,p0,q0,r0,s0,t0,u0,v0,w0,x0,y0,z0,aa0,ab0,ac0,ad0,ae0,af0,aj0,ah0,ai0,aj0,ak0,al0,am0,an0,ao0,ap0,aq0,ar0,as0,at0,au0]
                wt_to_csv(f0_csv,path_csv)
                if n>6:
                    break
                else:
                    pass
            n=n+1

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
    name='宽带链接'
    username='宽带帐号'
    password='宽带密码'
    disconnect_ADSL(name)
    connect_ADSL(name, username, password)


#主程序开始
#设置结果保存位置
t1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
global num
path_csv=r'D:\py\test3.csv'
with open(path_csv,'a') as f:
    f.close
driver_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
reconnect_ADSL()#重连ADSL
p=399
num=1
while p<401:
    url='https://www.amazon.com/s?k=hat&i=fashion-mens-accessories&rh=n%3A2474954011&page='+str(p)#关键词 hat
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),':开始采集第',p,'页')
    bs=find_bs(url,driver_path)
    #得出产品url列表
    ls=pro_ls(bs)
    for url in ls:
        #得出每一个产品的url，调用采集方法进行采集
        caiji_shopify(url)
        print('成功采集第',num,'条')
        num=num+1
        if num%10==0:
            reconnect_ADSL()#重连ADSL
        else:
            pass          
    print('成功写入第',p,'页')
    print('')
    p=p+1
t2=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print('采集完毕')
print('开始时间',t1)
print('结束时间',t2)
print('一个采集了',p,'个页面的',num,'条内容')
