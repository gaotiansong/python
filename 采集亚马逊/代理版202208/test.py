import requests
from lxml import etree
import re

def get_ip():
    url="http://api2.xkdaili.com/tools/XApi.ashx?apikey=XK0F329BE981ECF21718&qty=1&format=json&split=0&sign=fecf58a89e3e2c2ccb56e7d5a02a5757"
    reg=requests.get(url)
    s=reg.text
    ip=eval(s)["data"][0]["ip"]
    port=eval(s)["data"][0]["port"]
    return ip,port

def find_asin(fullurl):
    mo = re.compile('/dp/.*/')
    asin = mo.findall(fullurl)[0][4:-1]
    return asin

if __name__ == '__main__':
    print("你好")
    cookie = 'ubid-main=130-3719845-8792942; lc-main=en_US; session-id-apay=146-7066623-0357347; session-id=143-8826849-7592613; session-token=7vkC26oxsJ7R4xceOd1yCx2+Ldc4PJ7d6VKKk8nlIHp+xlKXVpvxleyFQcauPvqhafPpZkCsezx9wsj7rO62kVo7fPCq0iwwZnCCER4UkZhGf1qv1lfU5e+n8IDyOLJDGFNXzKyKNioS1mnC1nLHmx1bpFjd8zoA4L0DOXzeXAKzC9jaXVkYZQ+hslUtb5BwYI9hIxyPQHtPkvs1S+UcdZxslYPbHTzv; session-id-time=2082787201l; i18n-prefs=USD; csm-hit=tb:GXX4VEHAQHZXNXK90HA6+s-JJ75VSJQH71B37CWB4Q7|1661528678441&t:1661528678441&adb:adblk_no'
    headers = {
        "cookie": cookie,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    }
    url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=Sportswear&crid=X4KQE1PX1BW1&sprefix=sportswear%2Caps%2C305"
    n = 0
    while True:
        try:
            n = n + 1
            ip,port=get_ip()
            print(ip,port)
            proxy = {"http": "http://{ip}:{port}".format(ip=ip,port=port)}
            print("proxy==",proxy)
            reg = requests.get(url=url, headers=headers, timeout=10)
            print("reg",reg)
        except Exception as e:
            print("请求失败",e)
            continue
        if len(reg.text) < 100000:
            continue
        html = etree.HTML(reg.text)
        pro = html.xpath('//h2/a/@href')
        next_url = html.xpath('//*[@class="s-pagination-strip"]/a[contains(text(),"Next")]/@href')
        urls = []
        for i in pro:
            if r"/dp/" in i:
                print(find_asin(i))
                urls.append(find_asin(i))

        print(n, len(reg.text))
        print(len(urls))
        if not next_url:
            print("采集完毕")
            break
        print("next_url==", next_url)
        url = "https://www.amazon.com" + next_url[0]
