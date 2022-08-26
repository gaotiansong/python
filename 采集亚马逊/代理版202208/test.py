import requests
from lxml import etree
import re


def find_asin(fullurl):
    mo = re.compile('/dp/.*/')
    asin = mo.findall(fullurl)[0][4:-1]
    return asin


cookie = 'session-id=132-6253933-5694723; i18n-prefs=USD; ubid-main=133-7150600-1400460; lc-main=en_US; aws-target-data={"support":"1"}; AMCV_7742037254C95E840A4C98A6@AdobeOrg=1585540135|MCIDTS|19208|MCMID|62835205024466694032742511344581818736|MCAAMLH-1660099279|11|MCAAMB-1660099279|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1659501680s|NONE|MCAID|NONE|vVersion|4.4.0; aws-target-visitor-id=1659494479969-931829.38_0; aws-ubid-main=414-0546871-1584134; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6IjNhYWFiODU3LTRlZjItNGRjNi1iOTEwLTI4Y2IwYmZiNDM3ZSJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoicFN4Z1hxUlAzNnluME1sQUpubWZOOERYXC9mNXRnbFkybmM4XC9rYXpRb21ZPSIsImFybiI6ImFybjphd3M6aWFtOjozOTg1MDk0MDg3MjU6cm9vdCIsInVzZXJuYW1lIjoiYXdzdHdvIn0.6s0YGM1h1VstV0dCgV3M6FME8t524hRJwfA-942fq_gyeefBwUJmUiBJTqWNQaPtqCTQwUb5G6NMfM3ZKagFJdRK-IbAycVFCxks64r8ZMoVY9HRdQstyZJyen9Vsgci; aws-userInfo={"arn":"arn:aws:iam::398509408725:root","alias":"","username":"awstwo","keybase":"pSxgXqRP36yn0MlAJnmfN8DX/f5tglY2nc8/kazQomY\u003d","issuer":"http://signin.aws.amazon.com/signin","signinType":"PUBLIC"}; regStatus=registered; s_cc=true; s_nr=1661391740810-New; s_vnum=2093391740811&vn=1; s_dslv=1661391740813; s_sq=[[B]]; s_ppv=11; session-id-time=2082787201l; av-timezone=Asia/Shanghai; session-token=R/mTBQl5CThkxYNzbl5OLYocOBo1n9IaF847vcbiKDTb44ZfT6V39WgKBVwb1HBrWI/pUT5vYPG0bcpMY7CvqiaibfWYUiBJDRd3UhWOBzElDnaWdLmwjGpNVfqHpub5eBq23nBTeCAfPckeEdaq076XxoezHZaTE5Kp80Je9t/KHLI6oArlDvvnQur+t5qB1zJxJviy3vudoM/GmgZFWA/LasZYtDDJ; csm-hit=tb:ZVTHJD5Q2CM8PJY1YTC7+s-KZYZSS5QAE58V0R1G0Y3|1661489966242&t:1661489966242&adb:adblk_no'
headers = {
    "cookie": cookie,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}
url = "https://www.amazon.com/s?k=Athletic+Wear&rh=n%3A7141123011%2Cn%3A1046590&dc&ds=v1%3A%2BGAssHPeb2QvytQAofbisfxV4mSWckdd%2BK6xPyAeP9U&crid=3M8EQ5GKHUTIF&qid=1661524204&rnid=2941120011&sprefix=%2Caps%2C298&ref=sr_nr_n_2"
n = 0
while True:
    try:
        n = n + 1
        reg = requests.get(url=url, headers=headers, timeout=5)
    except:
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
