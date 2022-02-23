import csv
import re
from random import sample


def find_custom_keys(path):
    words = []
    with open(path, "r", encoding="utf-8") as f:
        rows = csv.reader(f)
        for key in rows:
            words.append(key[0].strip())
    return words


if __name__ == "__main__":
    pro_key = input("核心关键词（无素材产品名）：")
    pro_key = pro_key.strip()
    custom_keys = []
    if pro_key != "":
        custom_keys = find_custom_keys(pro_key)
    else:
        custom_keys = [""]
    # 获取各种关键词
    keywords_path = input("输入Search Terms所用关键词:")
    keywords_path = keywords_path.strip()
    keywords = find_custom_keys(keywords_path)

    # 专题风格
    zt_path = input("输入专题/风格词文件:")
    zt_path = zt_path.strip()
    zt1s = find_custom_keys(zt_path)

    # 场景词
    ch_path = input("输入场景词:")
    ch_path = ch_path.strip()
    ch1s = find_custom_keys(ch_path)

    # 要处理的文件
    pro_path = input("输入你要处理的文件:")
    pro_path = pro_path.strip()

    # 生成新文件路径和名称
    newpro_path = pro_path.split(r".")
    newpro_path = newpro_path[0] + r"New.csv"

    # 替换成新文件
    _ = open(newpro_path, "w", encoding="utf-8")

    custom1 = input("固定关键词1，出现在标题最前面，可直接回车跳过：")
    custom2 = input("固定关键词2，出现在素材标签后，可直接回车跳过：")
    custom3 = input("固定关键词3，出现在“For”前面，可直接回车跳过：")

    with open(pro_path, "r", encoding="gb18030") as f:
        pros = csv.reader(f)
        for p in pros:
            if p[0] == "Seller SKU" or p[0] == "item_sku":
                continue
            # print("p1",p[1])
            title = ""
            zt1 = sample(zt1s, 1)[0]  # 主题
            ch1 = sample(ch1s, 1)[0]  # 场合

            ns = [140, 160, 180]
            size_title = sample(ns, 1)[0]

            custom_key = sample(custom_keys, 1)[0]

            n = 0
            zt = []
            ch = []
            s1 = ""
            while True:
                n = n + 1
                zt.append(sample(zt1s, 1)[0])
                ch.append(sample(ch1s, 1)[0])
                # 拼凑的标题 p[1] 元素标题 custom_keys 核心关键词 p[2] 尺寸
                lss = [custom1] + [sample(custom_keys, 1)[0]] + [p[1]] + [custom2] + zt + [custom3] + ["For"] + ch + [
                    p[2]]
                s = " ".join(lss)
                s = s.strip()
                s = s.title().strip()
                s = re.sub("(\s)+", " ", s)
                print(n, size_title, len(s), "s=", s)
                break

            # 整理成型标题
            h1 = s
            print("最终标题", len(h1), "--", h1)

            # 生成关键词
            while True:
                ls_tags = []
                ls_tag = sample(keywords, 5)
                ls_tags1 = ls_tags
                ls_tags = ls_tags + ls_tag
                keys = ",".join(list(set(ls_tags)))
                if 150 < len(keys) < 250:
                    break
                elif len(keys) > 250:
                    keys = ",".join(ls_tags1)
                break
            with open(newpro_path, "a", newline="", encoding="utf8") as w:
                writer = csv.writer(w)
                # 拼凑的标题写入文件
                writer.writerow([p[0], p[1], h1, keys])
    input("处理完毕 按 Enter 退出")
