import csv
import multiprocessing
import os
import random
from multiprocessing import Pool
import queue

from PIL import Image


def cut_image(path, p):
    path_pic = path
    img_bg = Image.open(path_pic)
    w01, h01 = img_bg.size
    # 计算出截取框大小开始
    # 以w1为w2
    w2 = w01
    h2 = w2 / p
    if h2 > h01:
        h2 = h01
        w2 = h2 * p
    # 计算截取框大小完成
    print("计算截取框大小完成")
    left = (w01 - w2) / 2  # 左边离左边的距离
    up = 0
    right = w01 / 2 + w2 / 2
    below = h2
    im = img_bg.crop((int(left), int(up), int(right), int(below)))
    w, h = im.size
    s = w * h
    s1 = 1500 * 1500
    if s > s1:
        w001 = int((s1 * p) ** 0.5)
        h001 = int((s1 / p) ** 0.5)
        im = im.resize((w001, h001))
    print("背景大小:", im.size)
    return im


def custom_pic(bj, sc):
    # 把素材和底纹合成在一起
    custom_colour = ""
    # im = Image.open(path1)
    im = bj
    im = im.convert('RGBA')

    # img2 = Image.open(path2)
    img2 = sc
    img2 = img2.convert('RGBA')

    # img2 = img2.resize((1000, 1000))
    img_array = img2.load()
    # print("im.size=", im.size)
    # print("img2.size=", img2.size)

    width1, height1 = im.size  # 获取宽度和高度
    img2 = img2.resize((width1, height1))  # 元素背景一样大
    width2, height2 = img2.size

    img_array = img2.load()

    if custom_colour != "":
        for x in range(0, width2):
            for y in range(0, height2):
                rgb = img_array[x, y]  # 获取一个像素块的rgb
                r = rgb[0]
                g = rgb[1]
                b = rgb[2]
                a = rgb[3]
                if r != 0 or g != 0 or b != 0 or a != 0:  # 判断规则
                    img_array[x, y] = custom_colour

    x = int(width1 / 2 - width2 / 2)
    y = int(height1 / 2 - height2 / 2)
    im.paste(img2, (x, y), mask=img2)
    return im


def working(pic_name, path_dir1, path_dir2, pros):
    # q_name 图片完整名
    # path_dir1 素材文件夹
    # path_dir2 背景文件夹
    # pros 所有产品规格
    pig1_path = path_dir1 + r"/" + pic_name
    # 分离文件名和扩展名
    img_name, _ = os.path.splitext(pic_name)
    bg_files = os.listdir(path_dir2)
    new_path = path_dir1 + "new"
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    img1 = Image.open(pig1_path)
    w1, h1 = img1.size
    p1 = w1 / h1

    # 根据比例选择一个比例相似的产品图规格
    pro_ps = []
    for p2 in pros:
        # n1 是比例相差度
        n1 = abs(p1 - float(p2))
        # 把相差度满足条件度图片放入pic_bs中
        if n1 < 0.01:
            pro_ps.append(p2)
    # 从pro_ps中随机选择一种产品规格作为目标规格
    pro_p = float(random.sample(pro_ps, 1)[0])

    # 随机选择一张背景图 按目标规格裁剪
    b_img = random.sample(bg_files, 1)[0]
    # 拼接完整路径
    b_img_path = path_dir2 + r"/" + b_img
    print("获取的背景图:", b_img_path)
    # 通过裁剪 获得背景图
    bg_im = cut_image(b_img_path, pro_p)

    # 把素材合成到底纹图上
    img = custom_pic(bg_im, img1)  # 背景文件 素材文件

    if not os.path.exists(new_path + r"/" + str(pro_p)):
        os.mkdir(new_path + r"/" + str(pro_p))
    save_new_path = new_path + r"/" + str(pro_p) + r"/" + img_name + r".png"
    name_n = 0
    while os.path.exists(save_new_path):
        name_n = name_n+1
        save_new_path = new_path + r"/" + str(pro_p) + r"/" + img_name + str(name_n) + r".png"
    img.save(save_new_path)
    print("成功合成:", save_new_path)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    q = queue.Queue()
    # 拿到一个素材 计算其比例
    pig1_path_dir = input("请输入素材图文件夹路径:")
    # pig1_path_dir = r"D:\无框挂牌资料库\格言2021.12.7（1）"
    bg_dir_path = input("请输入底纹图文件夹:")
    # bg_dir_path = r"D:\无框挂牌资料库\木纹问题"
    pro_size_path = input("请输入产品规格列表文件:")
    # pro_size_path = r"D:\无框挂牌资料库\1.txt"
    p = input("请输入进程数(开多可能卡),可直接回车跳过:")
    if p == "":
        p = 1
    p = int(p)
    # 获取所有产品规格
    pro_sizes = []
    with open(pro_size_path) as f:
        rows = csv.reader(f)
        for row in rows:
            pro_sizes.append(row[0])
    # 从文件夹中获取一个素材
    for f_name in os.listdir(pig1_path_dir):
        q.put(f_name)
    pool = Pool(processes=p)
    while not q.empty():
        pool.apply_async(working, args=(q.get(), pig1_path_dir, bg_dir_path, pro_sizes))
    pool.close()
    pool.join()
    _ = input("执行完毕 按任意键退出")
