from fangfa import find_bs,find_bspro,find_urls,to_txt,panduan,find_h1,find_price,find_de,find_imgs,wt_csv
import re
from sitefull import site_full

patch_p,patch_txt,patch_pro,patch_csv,driver_path,ls_url,p1,p2=site_full()

while p1<=p2:
    url=ls_url+str(p1)
    p1=p1+1
    if panduan(url,patch_p):
        print('已存在，跳过:',url)
        continue
    else:
        to_txt(url+'\n',patch_p)
        pass

    n_y='y'#值为'y'表示下拉鼠标
    bs=find_bs(url,driver_path,n_y)
    print(type(bs))
    urls=find_urls(bs)
    for url in urls:
        url=r'https:'+url
        #把链接写入txt文件
        if panduan(url,patch_txt):
            print('已存在，跳过:',url)
            continue
        else:
            to_txt(url+'\n',patch_txt)
        print(url)

with open(patch_txt) as f:
    line=f.readline()
    n=0
    while line:
        url=line
        url=re.sub(r'\n','',url)
        n=n+1
        if panduan(url,patch_pro):
            print('已存在，跳过:',url)
            continue
        else:
            to_txt(url+'\n',patch_pro)
        #print(url)
        #获取产品页面bs对象
        #n_y='n'
        bs=find_bspro(url)
        #获取产品标题
        h1=find_h1(bs)
        #获取产品价格
        p=find_price(bs)
        #获取产品描述
        de=find_de(bs)
        #获取图片
        imgs=find_imgs(bs)
        try:
            file=[h1,p,de,'【seo分类】','【seo标签】',imgs]
            wt_csv(file,patch_csv)
        except:
            print('采集失败，跳过第',n-1,'条')
            pass
        line = f.readline()
