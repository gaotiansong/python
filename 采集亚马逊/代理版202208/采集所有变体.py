import requests
from lxml import etree
import re

url = "https://www.amazon.com/gp/product/B09XZM158C/ref?psc=1"
cookie = 'session-id=132-6253933-5694723; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=133-7150600-1400460; ' \
         'lc-main=en_US; aws-target-data={"support":"1"}; ' \
         'AMCV_7742037254C95E840A4C98A6@AdobeOrg=1585540135|MCIDTS|19208|MCMID|62835205024466694032742511344581818736' \
         '|MCAAMLH-1660099279|11|MCAAMB-1660099279|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT' \
         '-1659501680s|NONE|MCAID|NONE|vVersion|4.4.0; aws-target-visitor-id=1659494479969-931829.38_0; ' \
         'aws-ubid-main=414-0546871-1584134; ' \
         'aws-userInfo-signed' \
         '=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6IjNhYWFiODU3LTRlZjItNGRjNi1iOTEwLTI4Y2IwYmZiNDM3ZSJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoicFN4Z1hxUlAzNnluME1sQUpubWZOOERYXC9mNXRnbFkybmM4XC9rYXpRb21ZPSIsImFybiI6ImFybjphd3M6aWFtOjozOTg1MDk0MDg3MjU6cm9vdCIsInVzZXJuYW1lIjoiYXdzdHdvIn0.6s0YGM1h1VstV0dCgV3M6FME8t524hRJwfA-942fq_gyeefBwUJmUiBJTqWNQaPtqCTQwUb5G6NMfM3ZKagFJdRK-IbAycVFCxks64r8ZMoVY9HRdQstyZJyen9Vsgci; aws-userInfo={"arn":"arn:aws:iam::398509408725:root","alias":"","username":"awstwo","keybase":"pSxgXqRP36yn0MlAJnmfN8DX/f5tglY2nc8/kazQomY\u003d","issuer":"http://signin.aws.amazon.com/signin","signinType":"PUBLIC"}; regStatus=registered; session-token=xR7eYyxsSAkgb3+6xhG/LV5LYngH88gflKReuMAZHT+3McSbpMOdsyFSZDGgBEWyHPvXOUd1bX3BmMA1HtgNCcWya3jMcyDCuRV4KV1gSlGHMfBjWX42yFu8LxOhkt30fUnOPKl0CGexln4iHrQg/buIXhIuJnLHcXzXlgb1oU0TKC0opnMjx3xdofQY/hmL/Uu2TvXUAWV5vzWofZ/wWLFkZZLLsM8n; csm-hit=tb:ZVTHJD5Q2CM8PJY1YTC7+s-1RTA09JWD57STN3AY4CW|1661391509244&t:1661391509244&adb:adblk_no '
headers = {
    "cookie": cookie,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",

}
n = 0
while True:
    try:
        reg = requests.get(url=url, headers=headers, timeout=1)
        n = n + 1
    except:
        continue
    print(n, len(reg.text))
    html = etree.HTML(reg.text)
    title = html.xpath('//*[@id="productTitle"]')
    price = html.xpath('//*[@data-a-size="xl" and @data-a-color="base"]/span/text()')  # 第二个5  没有正确的
    img = html.xpath("//*[@class='a-button-inner']/span/img/@src")
    des = html.xpath('//*[@id="feature-bullets"]/ul/li/span/text()')
    try:
        title = title[0].text.strip()
        print("title=", title)
        print("price原始=", len(price), price)
        if len(price) > 1:
            price = price[1]
        elif len(price) == 1:
            price = price[0]
        else:
            price = 0
        img = img
        des = des
        try:
            mo_d = re.compile("\"dimensionValuesDisplayData\" : .*")
            js_d = mo_d.findall(reg.text)
            js_d = js_d[-1].strip()
            s1 = js_d[31:-1]
            asins = eval(s1)
        except:
            asins = ""
            print("asins==", asins)
    except Exception as e:
        print("e=", e,"\n")
        continue
    print("所有变体==", asins)
    print("标题==", title)
    print("价格==", price)
    print("图片==", len(img), img)
    print("描述==", des)
    print("\n")
