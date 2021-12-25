import csv
import os

from PIL import Image


def cut_image(get_ls, path, new_path):
    n = get_ls[0]
    path_pic = path + r"/" + get_ls[1]
    img = Image.open(path_pic)
    w1, h1 = img.size
    print(w1, h1)
    # 根据比例确定裁剪坐标
    with open("1.txt") as f:
        rows = csv.reader(f)
        for i in rows:
            p = float(i[0])
            print("p=", p)
            # 计算出截取框大小开始
            # 以w1为w2
            w2 = w1
            h2 = w2 / p
            if h2 > h1:
                h2 = h1
                w2 = h2 * p
            # 计算截取框大小完成
            left = (w1 - w2) / 2  # 左边离左边的距离
            up = 0
            right = w1 / 2 + w2 / 2
            below = h2
            im = img.crop((int(left), int(up), int(right), int(below)))
            # im.show()
            newpath = new_path + r"/" + str(p) + r"/"
            if not os.path.exists(newpath):
                os.mkdir(newpath)
            im.save(newpath + str(n) + r".png")


if __name__ == "__main__":
    from multiprocessing import Pool
    import queue

    q = queue.Queue()

    path = r"/Users/gaotiansong/Desktop/new_image/木纹"
    new_path = path + "_new"
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    n = 0
    for img in os.listdir(path):
        n = n + 1
        q.put([n, img])
        print([n, img])
    pool = Pool(processes=200)
    while not q.empty():
        pool.apply_async(cut_image, args=(q.get(), path, new_path))
    pool.close()
    pool.join()
