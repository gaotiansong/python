# -*-coding:utf-8 -*-
'''
2022/06/24更新
作者：一个哲学家
'''
import datetime

from lxml import etree

from selenium import webdriver
import time
import csv
from selenium.webdriver.chrome.service import Service


def find_driver():
    prefs = {"profile.managed_default_content_settings.images": 2}  # 设置无图模式
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)  # 无图
    options.add_argument("--lang=en")
    # options.add_argument("--headless")  # 不显示界面
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('ignore-certificate-errors')
    s = Service(r"C:\Users\Administrator\Desktop\1\chromedriver1.exe")  # 驱动器位置
    driver = webdriver.Chrome(service=s, options=options)
    return driver


def find_company(url_page, url_asin,c):
    print(datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S'), "请求", url_asin)
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    driver = find_driver()
    driver.get(url_asin)
    for c1 in c:
        driver.add_cookie(c1)
        print("成功添加",c1)
    driver.get(url_asin)
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    print("缓存==",driver.get_cookies())
    try:
        html = driver.page_source
        html2 = etree.HTML(html)
        coms = html2.xpath("//*[@id='sellerProfileTriggerId']")
        if len(coms) > 0:
            d = driver.find_element(By.XPATH, "//*[@id='sellerProfileTriggerId']")
            d.click()
            html3 = driver.page_source
            html4 = etree.HTML(html3)
            cs = html4.xpath("//*[@id='page-section-detail-seller-info']/div/div/div/div[*]/span")
            ls_s = []
            n = 0
            address = []
            for s in cs:
                if "Business Address" in s.text.strip() and n == 0:
                    ls_s.append(s.text.strip())
                    n = n + 1
                elif n == 0:
                    ls_s.append(s.text.strip())
                else:
                    address.append(s.text.strip())
            ad_s = " ".join(address)
            ls_s.append(ad_s)
            ls_s.append(url_page.strip())
            try:
                wt_csv(ls_s)
                print("成功保存:", ls_s)
            except Exception as e:
                print("保存失败:", e)
    except Exception as e:
        driver.close()
        driver.quit()
        print("内部出错跳过",e)

# 获取html
def find_html(url_html, page):
    print("请求{url}".format(url=url_html))
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    driver = find_driver()
    driver.get(url_html)
    # 调出输入框
    try:
        button1 = driver.find_element(by=By.XPATH, value="//*[@id='glow-ingress-block']")
    except Exception as e:
        print("查找邮编输入:", e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url_html, page)

    button1.click()
    # 输入邮编
    wait = WebDriverWait(driver, 10, 0.5)
    element = wait.until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))  # 等待
    element.send_keys("10041")
    # 点击发送
    button2 = driver.find_element(by=By.XPATH, value="//*[@id='GLUXZipUpdate']/span/input")
    WebDriverWait(driver, 10, 0.2).until(lambda driver1: button2.is_displayed())  # 显式等待
    button2.click()
    time.sleep(0.5)
    print("一次刷新")
    driver.refresh()
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
        return find_html(url_html, page)

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
            return find_html(url_html, page)
        ''''''
        if page == "ok":
            print("采集列表")
            # wait = WebDriverWait(driver, 10, 0.5)
            # element = wait.until(EC.presence_of_element_located((By.ID, "search")))
            # element.send_keys("selenium")
        ''''''
    # print("二次刷新")
    # driver.refresh()
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
        return find_html(url_html, page)
    try:
        html = driver.page_source
    except Exception as e:
        print("获取html:", e)
        print("开始关闭浏览器")
        driver.close()
        driver.quit()
        print("成功关闭浏览器")
        return find_html(url_html, page)

    print("html=", len(html))
    print("开始关闭浏览器")
    c=driver.get_cookies()
    print("c==",c)
    driver.close()
    driver.quit()
    print("成功关闭浏览器")
    html2 = etree.HTML(html)
    return html, html2,c


def find_asins_next_page(url_page):
    n = 0
    while True:
        n = n + 1
        print("n=", n)
        if n > 10:
            next_page_in = ""
            break
        try:
            print("开始请求：", url_page)
            page = "ok"
            _, html2,c= find_html(url_page, page)
        except Exception as e:
            print("获取html", e)
            next_page_in = ""
            time.sleep(1)
            continue

        xp_asins = html2.xpath("//*/div/@data-asin")
        asin_ls = []
        for i in xp_asins:
            if len(i) > 3:
                asin_ls.append(i)
        xp_page = html2.xpath("//*[@class='s-pagination-strip']/a/@href")
        if not xp_page:
            xp_page = html2.xpath("//*[@class='a-last']/a/@href")
        print("xp_page:", xp_page)
        try:
            next_page_in = "https://www.amazon.com" + xp_page[-1]
            print("next_page_in:", next_page_in)
            if len(next_page_in) > 0:
                print("成功采集下一页")
                break
        except EncodingWarning as e:
            print("e")
            next_page_in = ""
    return asin_ls, next_page_in,c


def wt_csv(data):
    with open(find_path(), "a", newline="", encoding="utf-8-sig") as f:
        wt = csv.writer(f)
        wt.writerow(data)


def find_path():
    # 设置文件保存路径
    path = r"C:\Users\Administrator\Desktop\1\探照灯.csv"
    return path


if __name__ == '__main__':
    import re

    # 文件保存路径
    page_url = "https://www.amazon.com/s?k=toy&i=toys-and-games&crid=123IE79BS52KF&sprefix=to%2Ctoys-and-games%2C650&ref=nb_sb_noss_2 "
    #page_url = "https://www.amazon.com/s?k=toy&i=toys-and-games&page=10&crid=123IE79BS52KF&qid=1656001824&sprefix=to%2Ctoys-and-games%2C650&ref=sr_pg_9"
    ls_page = []
    pg = []
    while True:
        if pg not in ls_page:
            ls_page.append(pg)
        else:
            print("全部采集完毕")
            break
        print("ls_page:", ls_page)
        asins, next_page,c= find_asins_next_page(page_url)
        print("asins:", asins)
        print("nextpage:", next_page)
        for asin in asins:
            print("asin==", asin)
            url_pro = "https://www.amazon.com/dp/" + asin
            try:
                find_company(page_url, url_pro,c)
            except Exception as e:
                print("外部出错跳过",e)
        page_url = next_page
        # 提取表示页数的 page=2
        mo = re.compile("page=\d{0,100}")
        pg = mo.findall(page_url)
