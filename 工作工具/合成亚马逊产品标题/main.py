import re
import csv
import Exec
from random import sample


def find_search_keywords(ls_keywords):
    # 生成关键词
    n2 = 0
    while True:
        n2 = n2 + 1
        ls_tags = []  # 关键词
        ls_tag = sample(ls_keywords, 5)
        ls_tags1 = ls_tags
        ls_tags = ls_tags + ls_tag
        keys = ",".join(list(set(ls_tags)))
        if 150 < len(keys) < 250:
            break
        elif len(keys) > 250:
            keys = ",".join(ls_tags1)
        if n2 > 5:
            break
    return keys


def find_custom_keys(path):
    words = []
    with open(path, "r", encoding="utf-8") as f_csv:
        rows = csv.reader(f_csv)
        for key in rows:
            words.append(key[0].strip())
    return words


def change_name(pro_name, size_name, custom_keys, zt1s, ch1s, custom1, custom2, custom3):
    ns = [140, 160, 180]
    size_title = sample(ns, 1)[0]

    n = 0
    zt = []  # 主题
    ch = []  # 场合
    while True:
        n = n + 1
        # 拼凑的标题 p[1] 元素标题 custom_keys 核心关键词 p[2] 尺寸
        if n == 1:
            lss = [sample(custom_keys, 1)[0]] + [pro_name] + [size_name]
        if n == 2:
            # 添加专题和场合词各一个
            lss = [sample(custom_keys, 1)[0]] + [pro_name] + zt + ["For"] + ch + [size_name]
        if n == 3:
            # 增加自定义词
            lss = [custom1] + [sample(custom_keys, 1)[0]] + [pro_name] + zt + ["For"] + ch + [size_name]
        if n == 4:
            lss = [custom1] + [sample(custom_keys, 1)[0]] + [pro_name] + [custom2] + zt + ["For"] + ch + [
                size_name]
        if n > 4:
            lss = [custom1] + [sample(custom_keys, 1)[0]] + [pro_name] + [custom2] + zt + [custom3] + ["For"] + ch + [
                size_name]

        s = " ".join(lss)
        s = s.strip()
        s = s.title().strip()
        s = re.sub("(\s)+", " ", s)
        s1 = s
        if len(s) > size_title:
            h1 = s1
            break
        if n > 10:
            break

        zt.append(sample(zt1s, 1)[0])
        ch.append(sample(ch1s, 1)[0])
        zt = list(set(zt))  # 去重
        ch = list(set(ch))  # 去重

    # 整理成型标题
    h1 = s
    print("最终标题", len(h1), "--", h1)
    return h1


if __name__ == "__main__":
    rd = Exec.ReadKeyWords(path=r"D:\Backup\桌面\keywords.xlsm")
    custom_keys = rd.get_words("核心词")
    ch1s = rd.get_words("场景词")
    zt1s = rd.get_words("风格词")
    keywords = rd.get_words("搜索词")
    while True:
        # 要处理的文件
        pro_path = input("输入你要处理的文件:")
        pro_path = pro_path.strip()
        if pro_path != "":
            break
        print("重试\n")
    # 生成新文件路径和名称
    newpro_path = pro_path.split(r".")
    newpro_path = newpro_path[0] + r"New.xlsm"

    # 替换成新文件
    _ = open(newpro_path, "w", encoding="utf-8")

    custom1 = input("固定关键词1，出现在标题最前面，可直接回车跳过：")
    custom2 = input("固定关键词2，出现在素材标签后，可直接回车跳过：")
    custom3 = input("固定关键词3，出现在“For”前面，可直接回车跳过：")

    EXEC = Exec.ReadExec(path=pro_path)
    print("red_data.c_name=", EXEC.c_name)
    for row in range(4, EXEC.Template.max_row+1):
        # 第四行开始是正文
        # 执行修改标题任务
        name = EXEC.Template.cell(row, EXEC.c_name).value  # 获取标题
        size_name = EXEC.Template.cell(row, EXEC.c_size_name).value  # 获取尺寸
        new_name = change_name(name, size_name, custom_keys, zt1s, ch1s, custom1, custom2, custom3)
        EXEC.Template.cell(row, EXEC.c_name).value = new_name

        # 执行生成 Search Terms 任务
        search_keywords = find_search_keywords(keywords)
        EXEC.Template.cell(row, EXEC.c_keywords).value = search_keywords
        print("name=", name)
        print("new_name=", new_name)

        print("search_keywords=", EXEC.Template.cell(row, EXEC.c_keywords).value)

    EXEC.sava_full(newpro_path)
