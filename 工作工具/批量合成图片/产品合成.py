import csv
import hashlib
import os
import time
import random

from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def custom_pro_pic(path_img, path_pic):
    # 获取一个场景图 场景图在外
    bg_img = Image.open(path_img)
    bg_img = bg_img.convert("RGBA")
    img_array = bg_img.load()
    w, h = bg_img.size
    pos = []
    for y in range(0, h):
        for x in range(0, w):
            rgb = img_array[x, y]  # 获取一个像素块的rgb
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            a = rgb[3]
            if a == 0:
                pos.append((x, y))
    # 确定左上第一个点
    p1xs = []
    p1ys = []
    for i in range(10):
        p1xs.append(pos[i][0])
        p1ys.append(pos[i][1])
    p1 = (min(p1xs) - 2, min(p1ys) - 2)  # 比最小小2像素
    # p1 = pos[1]

    # 确定右下第二个点
    p2xs = []
    p2ys = []
    for i in range(10):
        p2xs.append(pos[-i][0])
        p2ys.append(pos[-i][1])
    p2 = (max(p2xs) + 2, max(p2ys) + 2)  # 比最大大2像素
    w = p2[0] - p1[0]
    h = p2[1] - p1[1]

    # 获取 一个元素 元素在下 需要调整元素的位置
    im = Image.open(path_pic)
    im = im.convert('RGBA')
    try:
        im = im.resize((w, h))
    except Exception as e:
        print(e, p1, p2)

    bg1_img = Image.new("RGB", (32, 32), (255, 255, 255))
    bg1_img = bg1_img.resize(bg_img.size)

    # 合成1 合成底图
    bg1_img.paste(im, p1, mask=im)

    # 合成
    bg1_img.paste(bg_img, (0, 0), mask=bg_img)  # bg_img 在外
    return bg1_img


if __name__ == '__main__':
    # img_dir = r"/Users/gaotiansong/Desktop/jin挂牌素材new/1.0"  # 素材图文件夹
    img_dir = input("素材图文件夹:")
    img_dir = img_dir.strip()
    # bg_dir = "/Users/gaotiansong/Desktop/产品背景图"  # 背景图文件夹
    bg_dir = input("背景图文件夹:")
    bg_dir = bg_dir.strip()
    sku_f = input("输入SKU前缀(可用店铺名的一部分):")
    sku_f = sku_f.strip()
    pro_name = ""
    for img in os.listdir(img_dir):
        if "DS_Store" in img:
            continue
        print(img)
        pro_name = os.path.splitext(img)
        img = img_dir + r"/" + img

        now_date = time.strftime("%Y-%m-%d", time.localtime())
        pro_dir_root = bg_dir + "new"  # 产品图保存位置
        if not os.path.exists(pro_dir_root):
            # 创建文件夹用来保存所有的产品图
            os.mkdir(pro_dir_root)
        pro_dir = pro_dir_root + r"/" + now_date
        if not os.path.exists(pro_dir):
            os.mkdir(pro_dir)
        pro_rows = []
        for root in os.listdir(bg_dir):
            # 获取每一种尺寸规格
            if "DS_Store" in root:
                continue
            n = 0
            img_s = []
            pro_list = []
            for b in os.listdir(bg_dir + r"/" + root):
                n = n + 1
                # 获取每一张背景图
                if "DS_Store" in b:
                    continue
                pro_dir_a1 = pro_dir + r"/" + b
                bg = bg_dir + r"/" + root + r"/" + b
                new_img = custom_pro_pic(bg, img)
                sss = ''.join(random.sample(
                    ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g',
                     'f', 'e', 'd', 'c', 'b', 'a'], 5))
                img_name = root + str(n) + sss + str(time.time()).replace(r".", "_")
                img_new_path = pro_dir + r"/" + img_name + ".png"
                new_img.save(img_new_path)
                img_s.append(img_new_path)
            name = pro_name[0]
            pro_list.append(name)
            pro_list.append(sku_f + str(time.time()).replace(r".", ""))
            var_name = root
            pro_list.append(var_name)
            img_ls = img_s
            for im in img_ls:
                pro_list.append(im)
            pro_rows.append(pro_list)
            print("成功合成:", name)
        with open(pro_dir_root + r"/pro.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(pro_rows)
            writer.writerow([])
            print("成功合成:", pro_rows)
