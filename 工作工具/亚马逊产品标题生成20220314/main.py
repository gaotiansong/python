import Exec
from random import sample


def find_search_keywords(ls_keywords):
    # 生成搜索关键词
    n2 = 0
    ls_tags1 = []  # 关键词
    while True:
        n2 = n2 + 1
        ls_tags = sample(ls_keywords, 5)
        keys = ",".join(list(set(ls_tags + ls_tags1)))  # 去重且把关键词变成字符串
        if 100 < len(keys) < 250:
            break
        elif len(keys) > 250:
            keys = ",".join(ls_tags1)
        if n2 > 10:
            break
        ls_tags1 = ls_tags1 + ls_tags  # 把新的添加到旧的
        if len(keys) > 250:
            print(len(keys), "keys=", keys)
    return keys


def change_title(ls_keyword):
    s = (",".join(ls_keyword)).title()
    new_keyword = s.split(",")
    return new_keyword


def change_name(pro_name, sizename, core_word, ch1s, last_names, brand_words, longword):
    print("执行生成标题任务")
    # 处理大小写问题
    pro_name = pro_name.title()
    brand_words = brand_words.upper()
    core_word = change_title(core_word)
    ch1s = change_title(ch1s)

    if len(last_names) > 0:
        last_name = sample(last_names, 1)  # Accent 之后使用
    else:
        last_name = []
    ns = [120, 140, 160]
    size_title = sample(ns, 1)[0]

    # 构建标题成分
    lss = []
    core_word = sample(core_word, 1)[0]  # 核心词
    long_keyword = [""]  # 获取长尾词
    cjc_word = [""]  # 获取场景词

    long_keyword1 = []
    cjc_word1 = []
    n = 0
    while True:
        print("开始生成标题")
        # 标题 = 品牌(可选)+核心+素材+Accent(依赖产品名)+产品名(可选)+长尾词(可选，可多个)+for+场景(可选，可多个)+规格
        n = n + 1
        print("n=", n)
        if n == 1:
            # 核心词 + 素材名 + 尺寸
            # lss = [core_word] + [pro_name] + [sizename]
            lss = [brand_words] + [core_word] + [pro_name] + ["Accent"] + last_name + long_keyword + \
                  ["for"] + cjc_word + [sizename]
            print("lss=", lss)
            h1 = " ".join(lss)
            if size_title < len(h1) < 200:
                break
            else:
                long_keyword1 = long_keyword
                cjc_word1 = cjc_word
                continue
        elif n == 2:
            # 增加 last_name 即产品的其它叫法 出现在 Accent 后面
            # lss = [core_word] + [pro_name] + ["Accent"] + last_name + [sizename]
            lss = [brand_words] + [core_word] + [pro_name] + ["Accent"] + last_name + long_keyword + \
                  ["for"] + cjc_word + [sizename]
            h1 = " ".join(lss)
            if size_title < len(h1) < 200:
                break
            elif len(h1) > 200:
                long_keyword = long_keyword1
                cjc_word = cjc_word1
                break
            else:
                long_keyword1 = long_keyword
                cjc_word1 = cjc_word
                continue
        elif n == 3:
            # 增加 cjc_words 即场景词 出现在for 后面
            cjc_word.append(sample(ch1s, 1)[0])
            cjc_word = list(set(cjc_word))
            # lss = [core_word] + [pro_name] + ["Accent"] + last_name + ["for"] + cjc_word + [sizename]
            lss = [brand_words] + [core_word] + [pro_name] + ["Accent"] + last_name + long_keyword + \
                  ["for"] + cjc_word + [sizename]
            h1 = " ".join(lss)
            if size_title < len(h1) < 200:
                break
            elif len(h1) > 200:
                long_keyword = long_keyword1
                cjc_word = cjc_word1
                break
            else:
                long_keyword1 = long_keyword
                cjc_word1 = cjc_word
                continue
        elif n == 4:
            # 增加 long_keyword 即长尾词 出现在 for 前面
            long_keyword.append(sample(longword, 1)[0])
            long_keyword = list(set(long_keyword))  # 去重
            lss = [brand_words] + [core_word] + [pro_name] + ["Accent"] + last_name + long_keyword + \
                  ["for"] + cjc_word + [sizename]
            h1 = " ".join(lss)
            if size_title < len(h1) < 200:
                break
            elif len(h1) > 200:
                long_keyword = long_keyword1
                cjc_word = cjc_word1
                break
            else:
                long_keyword1 = long_keyword
                cjc_word1 = cjc_word
                continue
        else:
            if n > 20:
                break
            if n % 2 == 1:
                # 增加 cjc_words
                cjc_word.append(sample(ch1s, 1)[0])
                cjc_word = list(set(cjc_word))
            else:
                # 增加 long_keyword 和 场景词
                long_keyword.append(sample(longword, 1)[0])
                long_keyword = list(set(long_keyword))  # 去重

            lss = [brand_words] + [core_word] + [pro_name] + ["Accent"] + last_name + long_keyword + \
                  ["for"] + cjc_word + [sizename]
            h1 = " ".join(lss)
            if size_title < len(h1) < 200:
                break
            elif len(h1) > 200:
                long_keyword = long_keyword1
                cjc_word = cjc_word1
                break
            else:
                long_keyword1 = long_keyword
                cjc_word1 = cjc_word
                continue
    # 整理成型标题
    core_word = core_word+"|"
    long_keyword = ["|".join(long_keyword)]
    cjc_word = ["|".join(cjc_word)]
    ok_h1 = [brand_words] + [core_word] + [pro_name] + ["Accent"] + last_name + long_keyword + \
            ["for"] + cjc_word + [sizename]
    print("ok_h1=", ok_h1)
    if ok_h1[4] == "":
        ok_h1[3] = ""
    if ok_h1[-2] == "":
        ok_h1[-3] = ""
    ok_h = []
    for i in ok_h1:
        if i:
            ok_h.append(i)
    h1 = " ".join(ok_h)
    print(row, "计划长度", size_title, "最终标题", len(h1), "--", h1)
    return h1


if __name__ == "__main__":
    while True:
        # 要处理的文件
        word_path = input("请输入你的关键词表格:")
        word_path = word_path.strip()
        if word_path != "":
            break
        print("重试\n")

    cjc_max = input("提取场景词数量(默认可跳过):")
    if cjc_max != "":
        cjc_max = int(cjc_max)
    else:
        cjc_max = 0
    rd = Exec.ReadKeyWords(path=word_path)
    custom_keys = rd.get_words("核心词")

    keywords = rd.get_words("搜索词")
    long_words = rd.get_words("长尾词")

    while True:
        # 要处理的文件
        pro_path = input("输入你要处理的亚马逊表格:")
        pro_path = pro_path.strip()
        if pro_path != "":
            break
    # 生成新文件路径和名称
    newpro_path = pro_path.split(r".")
    newpro_path = newpro_path[0] + r"New.xlsm"
    brand_name = input("品牌名，出现在标题最前面，可直接回车跳过：")
    EXEC = Exec.ReadExec(path=pro_path)

    for row in range(4, EXEC.Template.max_row + 1):
        cjc_all_words = rd.get_words("场景词")
        if cjc_max > len(cjc_all_words) or cjc_max == 0:
            cjc_max = len(cjc_all_words)
            print("实际使用场景词:", cjc_max)
        cjc_words = sample(cjc_all_words, cjc_max)
        if cjc_words == [None]:
            cjc_words = []
        print("场景词:", cjc_words)

        pro_name_words = rd.get_words("产品名")

        # 第四行开始是正文
        # 执行修改标题任务
        name = EXEC.Template.cell(row, EXEC.c_name).value  # 获取标题
        name = name.strip()
        size_name = EXEC.Template.cell(row, EXEC.c_size_name).value  # 获取尺寸
        try:
            # 用来处理空行问题
            print("row=", row)
            new_name = change_name(name, size_name, custom_keys, cjc_words, pro_name_words, brand_name, long_words)
        except Exception as e:
            print(e)
            continue
        new_name = new_name.strip()
        EXEC.Template.cell(row, EXEC.c_name).value = new_name

        # 执行生成 Search Terms 任务
        search_keywords = find_search_keywords(keywords)
        EXEC.Template.cell(row, EXEC.c_keywords).value = search_keywords
        print("name=", name)
        if ("Cup" or "Mug") in name:
            print("不修改")
            new_name = name
        print("new_name=", new_name)

        print("search_keywords=", EXEC.Template.cell(row, EXEC.c_keywords).value)

    EXEC.sava_full(newpro_path)
    _ = input("按任意键退出")
