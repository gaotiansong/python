import os
import csv
import sys
from pathlib import Path
import re


def wt_csv(path, data):
    with open(path, "a", newline="") as f:
        wt = csv.writer(f)
        wt.writerow(data)


# 遍历文件夹下文件方法
def get_file_list(p, file_list):
    p = str(p)
    if p == "":
        return []
    # p = p.replace(" -", "\\")
    if p[-1] != "\\":
        p = p + "\\"
    files = os.listdir(p)
    for f in files:
        if os.path.isfile(p + f):
            file_list.append({'path': p, 'file': f})
        else:
            get_file_list(p + f, file_list)
    return file_list


# DFA过滤敏感词算法
class DFAFilter(object):
    def __init__(self):
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '\x00'  # 限定

    def add(self, keyword):
        keyword = keyword.lower()  # 关键词英文变为小写
        chars = keyword.strip()  # 关键字去除首尾空格和换行
        if not chars:  # 如果关键词为空直接返回
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars.split(" "))):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars.split(" ")[i] in level:
                level = level[chars.split(" ")[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars.split(" "))):
                    level[chars.split(" ")[j]] = {}
                    last_level, last_char = level, chars.split(" ")[j]
                    level = level[chars.split(" ")[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars.split(" ")) - 1:
            level[self.delimit] = 0

    def parse(self):
        for keyword in infringing_word_list:
            self.add(str(keyword).strip())

    def filter(self, message, repl=""):
        message = message
        ret = []
        start = 0
        while start < len(message.split(" ")):
            level = self.keyword_chains
            step_ins = 0
            for char in message.split(" ")[start:]:
                if char.lower().replace(',', '') in level:
                    step_ins += 1
                    if self.delimit not in level[char.lower().replace(',', '')]:
                        level = level[char.lower().replace(',', '')]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message.split(" ")[start] + " ")
                    break
            else:
                ret.append(message.split(" ")[start])
            start += 1

        return ''.join(ret)


if __name__ == "__main__":
    import enchant
    # 拼写检测 设置语种
    checker = enchant.Dict("en_US")
    print(checker.check("hello"))
    print(enchant.list_languages())

    maxInt = sys.maxsize
    # CSV 文件读取最大值设置
    while True:
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    # 要处理的文件列表
    old_path = r"D:\Backup\桌面\220105"
    input_old_path = input("输入要处理的文件夹：")
    if input_old_path != "":
        old_path = input_old_path
    old_path = old_path.replace(r'"', '')
    # 结果保存地址
    new_path = old_path + "_New"
    if os.path.exists(new_path):
        pass
    else:
        os.mkdir(new_path)
    # 侵权词列表
    infringing_path = r'./infringing_word_list.txt'

    # 侵权词列表
    with open(infringing_path, 'r', encoding='utf-8') as fl:
        data = fl.readlines()
    infringing_word_list = list(data)
    infringing_word_list = [c.replace('\n', '') for c in infringing_word_list]

    gfw = DFAFilter()
    gfw.parse()

    # 遍历出来的文件列表
    file_list_ = []
    result = {}
    # 获取文件列表
    get_file_list(old_path, file_list_)
    print("要处理的文件:", file_list_)
    # 遍历文件
    for file in file_list_:
        # 提取店铺名
        print("file=", file)
        shop = "shop_list[key]"
        # 提取站点 即获取 All+Listings+HNTGJRT-ca.txt 中 的 ca
        region = file["file"][-6:-4].lower()
        # 店铺是否在需要处理的店铺列表里
        if 'All+Listings' in file["file"] or '所有商品报告' in file["file"]:
            if shop not in result:
                result[shop] = {}
            if region not in result[shop]:
                result[shop][region] = {'Listings': [], 'BusinessReport': []}
            result[shop][region]['Listings'].append(file)
    # 需要处理文件的列表 key = 店铺名字
    for key in result:
        # 遍历店铺下站点
        for region in result[key]:
            # 读取all_listing
            # 没文件 跳过
            if len(result[key][region]['Listings']) == 0:
                continue
            # 遍历该站点all_listing文件
            for l in result[key][region]['Listings']:
                # 结果保存地址
                new_path_file = os.path.join(new_path, l['file'] + " update.csv")
                print("保存地址:", new_path_file)
                # 结果已存在跳过
                if os.path.exists(new_path_file):
                    print('%s\t%s\t%s\t%s\t%s' % (key, region, l['path'], l['file'], new_path_file))
                    continue
                # all_listing文件地址
                listings_file_ = l['path'] + l['file']
                # 读取 all_listing 文件
                try:
                    with open(listings_file_, 'r', encoding='utf-8') as fl:
                        listing_list = csv.reader(fl, delimiter='\t')
                        listing_list = list(listing_list)
                    fl.close()
                except Exception as e:
                    print(e)
                    with open(listings_file_, 'r', errors='ignore') as fl:
                        listing_list = csv.reader((line.replace('\x00', '') for line in fl), delimiter='\t')
                        listing_list = list(listing_list)
                    fl.close()
                # 英语站点处理
                if region in ['us', 'ca', 'uk']:
                    for listing in listing_list[1:]:
                        # listing 表格中的一行
                        print("listing===", listing)
                        # 标题拼写检测 word_list 是组成标题的单词列表
                        print("处理前标题:",listing[0])
                        # 把标题中的逗号变成空格
                        title = re.sub(","," ",listing[0])
                        word_list = title.split(' ')
                        print("word_list=",word_list)
                        new_title = ''
                        # 取出标题中的每一个单词进行检查
                        for word in word_list:
                            word_replace = word.replace(',', '')
                            print("要检查的词：",word_replace)
                            if word_replace:
                                if checker.check(word_replace):
                                    # 把处理后的词再次组成句子
                                    print("获取一个词",word)
                                    new_title = new_title + word + ' '
                        print("拼写检查后的标题:",new_title)
                        # 标题侵权词过滤
                        new_title = gfw.filter(new_title)
                        listing[0] = new_title
                        print("处理后的标题：",new_title)

                        # 描述拼写检测
                        word_list = listing[1].split(' ')
                        new_description = ''
                        for word in word_list:
                            # 删除关键词中的逗号
                            word_replace = word.replace(',', '')
                            if word_replace:
                                if checker.check(word_replace):
                                    new_description = new_description + word + ' '

                        # print(new_description)
                        # 描述侵权词过滤
                        new_description = gfw.filter(new_description)
                        # print(new_description)
                        listing[1] = new_description
                # 保存结果， 英语语种为处理结果，其他为原始文件
                with open(new_path_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(listing_list)
                print('%s\t%s\t%s\t%s\t%s' % (key, region, l['path'], l['file'], new_path_file))
                # 保存成功结果 successfull
                successfull = os.path.join(new_path, "successfull.csv")
                wt_csv(successfull, [l['file']])
            # 保存
    print("成功处理文件夹{}".format(file_list_))
    _ = input("按任意键退出")
