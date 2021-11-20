# -*-coding:utf-8 -*-
from os import path, write
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from lxml import etree
import re

def find_driver():
    #press = {"profile.managed_default_content_settings.images": 2}  #设置无图模式
    options = webdriver.ChromeOptions()
    #options.add_experimental_option("press", press)
    options.add_argument("--lang=en")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(options=options,
                              executable_path=r'D:\Users\ZG\PycharmProjects\pythonProject\chromedriver.exe')
    return driver


# 获取html
def find_html(url,keyword):
    print("请求{url}".format(url=url))
    driver = find_driver()
    driver.get(url)
    # 调出输入框
    try:
        button1 = driver.find_element_by_xpath("//*[@id='glow-ingress-block']")
    except Exception as e:
        print("查找邮编输入:", e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url,keyword)

    button1.click()

    # 输入邮编
    wait = WebDriverWait(driver, 10, 0.5)
    element = wait.until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))  #等待
    element.send_keys("10041")
    # 点击发送
    button2 = driver.find_element_by_xpath("//*[@id='GLUXZipUpdate']/span/input")
    WebDriverWait(driver, 10, 0.2).until(lambda driver: button2.is_displayed())  #显式等待
    button2.click()
    time.sleep(0.5)
    print("一次刷新")
    driver.refresh()

    #输入关键词
    wait1 = WebDriverWait(driver, 10, 0.5)
    element = wait1.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))  # 等待
    element.send_keys(keyword)
    # 点击发送
    button2 = driver.find_element_by_xpath("//*[@id='nav-search-submit-button']")
    WebDriverWait(driver, 10, 0.2).until(lambda driver: button2.is_displayed())  # 显式等待
    button2.click()

    try:
        driver.implicitly_wait(30)
        driver.set_script_timeout(30)
        driver.set_page_load_timeout(30)
    except Exception as e:
        print("超时:", e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url,keyword)

    a = 0
    while a < 1:
        try:
            print("下拉", a)
            a = a + 1

            driver.execute_script(
                "window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*1/5); var "
                "lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            driver.execute_script(
                "window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*2/5); var "
                "lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            driver.execute_script(
                "window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*3/5); var "
                "lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            driver.execute_script(
                "window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*4/5); var "
                "lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)
            driver.execute_script(
                "window.scrollTo(document.body.scrollHeight, document.body.scrollHeight); var "
                "lenOfPage=document.body.scrollHeight; return lenOfPage;")

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return "
                "lenOfPage;")
            time.sleep(0.01)

            # 上拉到顶部
            print("上拉")
            driver.execute_script(
                "window.scrollTo(document.body.scrollHeight, document.body.scrollHeight*4/5); var "
                "lenOfPage=document.body.scrollHeight; return lenOfPage;")
            time.sleep(0.01)

        except Exception as e:
            print("拉动:", e)
            print("开始关闭浏览器")
            driver.close()
            driver.quit()
            print("成功关闭浏览器")
            return find_html(url,keyword)
    try:
        driver.implicitly_wait(5)
        driver.set_script_timeout(5)
        driver.set_page_load_timeout(5)
    except Exception as e:
        print("超时:", e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url,keyword)
    try:
        html = driver.page_source
    except Exception as e:
        print("获取html:", e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url,keyword)

    print("html=", len(html))
    print("开始关闭浏览器")
    driver.close()
    driver.quit()
    print("成功关闭浏览器")
    html2 = etree.HTML(html)
    return html, html2


def find_num(html1,html2):
    print("开始筛选内容")
    html1=html1
    numbers=html2.xpath('//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]/text()')       
    numb=""
    try:
        numb=numbers[0]
    except Exception as e:
        print(e)
    print("筛选完毕")
    return numb

def wt_csv(path,data):
    with open(path,"a",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(data)

import csv
url=r"https://www.amazon.com/"

with open(r"C:\Users\ZG\Desktop\在线品牌词库.csv","r") as f:
    rows=csv.reader(f)
    for i in rows:
        try:
            keyword=i[0].strip()
        except Exception as e:
            print(e)
        
        html1,html2=find_html(url,keyword)
        numb=find_num(html1,html2)
        #从numb中筛选出结果数
        print("原始n=",numb)
        mo=re.compile("of .+ results")
        n=mo.findall(numb)
        try:
            n=re.sub("of|over|results","",n[0])
            n=n.strip()
        except Exception as e:
            print(e)
            n=numb
        data=[keyword,n]
        print(data)
        path=r"C:\Users\ZG\Desktop\亚马逊上架工具\筛选常用词\筛选后.csv"
        wt_csv(path,data)
