from PIL import Image
import os
import random
import time


def custom_pic(path1, path2, pic, save_path):
    print("开始执行合成函数")
    custom_colour = ""

    img1 = Image.open(path1)
    img1 = img1.convert('RGB')
    # img1 = img1.resize((2000, 2000))  # 注意，是2个括号

    img2 = Image.open(path2)
    img2 = img2.convert('RGB')
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
        # 元素都宽比背景都宽大
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
    img1.save(save_path + "/" + pic)
    print("成功合成:", pic)
    time.sleep(3)


def get_w_h(img_path):
    img = Image.open(img_path)
    w, h = img.size
    return w / h


if __name__ == "__main__":

    dir1 = input("请输入背景图文件夹地址:")
    dir2 = input("请输入素材文件夹地址:")
    path1_dir = dir1.strip()
    path2_dir = dir2.strip()
    # path1_dir = r"/Users/gaotiansong/Desktop/new_image/木纹"
    # path2_dir = r"/Users/gaotiansong/Desktop/new_image/1417x1890"
    save_path = path2_dir + "new"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for pic in os.listdir(path2_dir):
        back = random.sample(os.listdir(path1_dir), 1)[0]
        path1 = path1_dir + "/" + back

        path2 = path2_dir + "/" + pic
        # n1 用来表示张图片的比例相似度
        n1 = abs(get_w_h(path2) - get_w_h(path1))
        # n 用来表示查找背景的最大次数 如果查找100找不到适合的背景 ，就不考虑相似度了
        n=0
        while n1 > 0.001 and n< 100:
            n=n+1
            back = random.sample(os.listdir(path1_dir), 1)[0]
            path1 = path1_dir + "/" + back
            n1 = abs(get_w_h(path2) - get_w_h(path1))
            print("n1:",n1)
        custom_pic(path1, path2, pic, save_path)
