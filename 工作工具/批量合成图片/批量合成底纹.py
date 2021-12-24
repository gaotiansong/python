from PIL import Image
import os
import random
import time
import re
import multiprocessing as mp


def custom_pic(path1, path2, pic, save_path):
    custom_colour = ""
    img1 = Image.open(path1)
    img1 = img1.convert('RGBA')
    # img1 = img1.resize((2000, 2000))  # 注意，是2个括号

    img2 = Image.open(path2)
    img2 = img2.convert('RGBA')
    # img2 = img2.resize((1000, 1000))
    img_array = img2.load()

    width1, height1 = img1.size  # 获取宽度和高度
    width2, height2 = img2.size  # 获取宽度和高度
    # 长宽都比背景大
    if width2 > width1 and height2 > height1:
        # 以背景宽为元素宽
        if width2 / width1 > height2 / height1:
            w2 = width1
            p = width1 / width2
            h2 = height2 * p
            img2 = img2.resize((int(w2), int(h2)))
        # 以背景高为元素高
        else:
            h2 = height1
            p = height1 / height2
            w2 = width2 * p
            img2 = img2.resize((int(w2), int(h2)))
    # 长或者宽比背景大
    elif width2 > width1 or height2 > height1:
        # 元素的宽比背景的宽大
        if width2 > width1:
            w2 = width1
            p = width1 / width2
            h2 = height2 * p
            img2 = img2.resize((int(w2), int(h2)))
        else:
            h2 = height2
            p = height1 / height2
            w2 = width2 * p
            img2 = img2.resize((int(w2), int(h2)))

    width1, height1 = img1.size  # 获取宽度和高度
    width2, height2 = img2.size  # 获取宽度和高度
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
    img1.paste(img2, (x, y), mask=img2)
    # img1.show()
    pic = re.sub(r".jpg", r".png", pic)
    img1.save(save_path + "/" + pic)
    print("成功合成:", pic)
    time.sleep(3)


# 获取图片的宽比高的比例
def get_w_h(img_path):
    img = Image.open(img_path)
    w, h = img.size
    return w / h


# 工作函数
def working(pic, path1_dir, path2_dir, save_path):
    path2 = path2_dir + "/" + pic
    n1 = 100
    n2 = 0.01
    while n1 > n2:
        # 从所有底纹文件夹中随机抽取一个文件夹
        backs = random.sample(os.listdir(path1_dir), 5)
        for back in backs:
            try:
                float(back)
            except Exception as e:
                print(e)
                continue
            n1 = abs(get_w_h(path2) - float(back))
            if n1 < n2:
                print("差异度：", n1)
                # 差异度不超过某个值时就可以选择该文件夹 然后从该文件夹中随机抽取一张图片
                back_pic_path = path1_dir + r"/" + back  # 具体规格的底纹图文件夹
                # 从该规格的底纹文件夹中随机抽取一张图片
                back_pic = random.sample(os.listdir(back_pic_path), 1)[0]
                path1 = back_pic_path + "/" + back_pic
                custom_pic(path1, path2, pic, save_path)
                break


if __name__ == "__main__":
    from multiprocessing import Pool
    import queue

    q = queue.Queue()
    dir1 = input("请输入底纹文件夹地址:")
    dir2 = input("请输入素材文件夹地址:")
    path1_dir = dir1.strip()
    path2_dir = dir2.strip()
    # path1_dir = r"/Users/gaotiansong/Desktop/new_image/木纹"
    # path2_dir = r"/Users/gaotiansong/Desktop/new_image/1417x1890"
    save_path = path2_dir + "new"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for pic in os.listdir(path2_dir):
        q.put(pic)
    pool = Pool(processes=10)
    while not q.empty():
        # 只要队列不空 一直提交进程执行
        pool.apply_async(working, args=(q.get(), path1_dir, path2_dir, save_path))
    pool.close()
    pool.join()
