from PIL import Image
import os
import shutil
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
    img_deal.save('{new_dir}\switch_{file_name}'.format(new_dir=new_dir,file_name=file_name))

#需要修改的文件夹
#now_path = r"D:\Backup\桌面\test\\"
now_path=input('请输入文件夹路径：')
new_path = os.mkdir(now_path + '\\' + 'new_img')
new_dir = now_path + '\\' + 'new_img'
# 遍历文件夹下的文件，并判断是否是JPG文件
for file_name in os.listdir(now_path):
    files_path = now_path + '\\' + file_name
    if 'jpg' in files_path:
        x,y=size_n(files_path)
        smaller_img(x, y, files_path,new_dir)
        # 遍历文件来判断是否是转换后的jpg文件
        for move_name in os.listdir(now_path):
            move_path = now_path + '\\' + move_name
            if 'switch' in move_path:
                shutil.move(move_path,new_dir)
            else:
                 print(move_path, '无须移动')
        print(file_name, 'switch success')
    else:
        print(file_name, 'is not img')
