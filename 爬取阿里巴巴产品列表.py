from selenium import webdriver
import time,bs4,os,csv
from selenium.webdriver.chrome.options import Options
def pro_urls(n):
    opt = webdriver.ChromeOptions()
    opt.add_argument("--headless") #设置无界面模式
    opt.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',options=opt) #驱动器路径
    url = "https://www.alibaba.com/products/Basketball_Jersey.html?spm=a2700.galleryofferlist.0.0.3d492c63yoMZNz&IndexArea=product_en&page="+str(n)
    driver.get(url)
    time.sleep(3)
    a=0
    while a<5:
        #下拉鼠标
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        time.sleep(1)
        a=a+1
    html=driver.page_source
    bs=bs4.BeautifulSoup(html,'html.parser')
    prourls=bs.select('.organic-gallery-title')
    i=0
    for prourl in prourls:
        #print('https:'+prourl.get('href'))
        file=['https:'+prourl.get('href')]
        #调用方法把内容写入csv文件
        writer_pro('你的文件路径\url.csv',file)
    driver.quit()
    
#把内容写入csv文件的方法
def writer_pro(site,file):
    headfile=['url']
    csvf=open(site,'a',newline='')#newline=''去除空格
    size=os.path.getsize(site)
    writer=csv.writer(csvf)
    if size==0:
        writer.writerow(headfile)
        writer.writerow(file)
        csvf.close()
    else:
        writer.writerow(file)
        csvf.close()
n=1
while n<=100:
    pro_urls(n)
    print('采集完',n,'页')
