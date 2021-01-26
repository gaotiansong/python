from PIL import Image
import os
import shutil
from random import choice
import string

def generate_passwd(passwd,passwd_length):
    passwd_lst = []
    while (len(passwd_lst) < passwd_length):
        passwd_lst.append(choice(passwd))   #把循环出来的字符插入到passwd_lst列表中
    return ''.join(passwd_lst)            #通过''.join(passwd_lst)合并列表中的所有元素组成新的字符串

def passwd_out(passwd_length,passwd_count,zm,sz):
    if zm!=None:
        Letter = string.ascii_letters   #通过string.ascii_letters 获取所有因为字符的大小写字符串 'abc....zABC.....Z'
    else:
        Letter=''
    if sz!=None:
        number = string.digits          #通过string.digits 获取所有的数字的字符串 如：'0123456789'
    else:
        number=''

    passwd = Letter + number   #定义生成密码是组成密码元素的范围   字符+数字+大小写字母
    pwds=[]
    for _ in range(0,passwd_count):
        pwds.append(generate_passwd(passwd,passwd_length))
    return pwds

def size_n(filename):
    from PIL import Image
    im = Image.open(filename)#返回一个Image对象
    w1=im.size[0]
    h1=im.size[1]
    n1=w1/2000
    n2=h1/2000
    #计算出等比例缩放后大小

    if n1<=n2:
        w=int(w1/n1)
        h=int(h1/n1)
    else:
        w=int(w1/n2)
        h=int(h1/n2)
    return w,h
# 修改图片大小
def smaller_img(x, y, path,new_dir):
    path = str(path)
    old_img = Image.open(path)
    img_deal = old_img.resize((x, y), Image.ANTIALIAS)
    img_deal = img_deal.convert('RGB')
    new_file_name=passwd_out(30,1,'','')[0]+r'.jpg'
    img_deal.save('{new_dir}/{file_name}'.format(new_dir=new_dir,file_name=new_file_name))

while True:
    #需要修改的文件夹
    #now_path = r"D:\Backup\桌面\test\\"
    now_path=input('请输入文件夹路径：')
    now_path=now_path.strip()
    now_path=now_path.replace('\"', '')
    print(now_path)
    #获取文件夹名
    _,f=os.path.split(now_path)
    new_img='ok_'+f
    #如果新文件夹存在则删除，不存在则创建
    if os.path.lexists(now_path + '\\' + new_img):
        shutil.rmtree(now_path + '\\' + new_img)
        new_path = os.mkdir(now_path + '\\' + new_img)
    else:
        new_path = os.mkdir(now_path + '\\' + new_img)
    new_dir = now_path + '\\' + new_img
    # 遍历文件夹下的文件，并判断是否是JPG文件
    list_file=os.listdir(now_path)
    for file_name in list_file:
        files_path = now_path + '\\' + file_name
        if r'.jpg' in files_path:
            #获取图片长、宽
            x,y=size_n(files_path)
            #设置图片长、宽
            smaller_img(x, y, files_path,new_dir)
            print(file_name, 'success')
        else:
            print(file_name, 'is not img')
