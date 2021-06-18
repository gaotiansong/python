def site_full():
    #设置已经采集过的页面存放位置
    patch_p=r'/Users/gaotiansong/Desktop/p.txt'

    #设置产品url存放位置
    patch_txt=r'/Users/gaotiansong/Desktop/test_url.txt'
    open(patch_txt,'a')

    #设置已经采集过的产品保存位置
    patch_pro=r'/Users/gaotiansong/Desktop/url_db.txt'

    #设置结果csv保存位置
    patch_csv=r'/Users/gaotiansong/Desktop/jerseys_pro.csv'

    #设置驱动器路径，chromedriver需要下载
    driver_path=r'/Users/gaotiansong/Downloads/chromedriver'

    #设置要采集的分类url,不包括'='后面的数字
    ls_url=r'https://www.alibaba.com/products/print_on_demand_t_shirt.html?spm=a2700.galleryofferlist.0.0.59b77793XlXh8y&IndexArea=product_en&page='

    #设置起始页
    p1=1

    #设置结束页
    p2=100
    return patch_p,patch_txt,patch_pro,patch_csv,driver_path,ls_url,p1,p2
