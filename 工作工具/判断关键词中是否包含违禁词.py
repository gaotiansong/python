#coding=utf-8
import csv
import time
import re

def find_words(s):
    #计算一段文字所有相邻组合
    words=[]
    s=re.sub("\s+"," ",s)
    s_ls=s.split(" ")
    size=len(s_ls)
    for i in range(size):
        i=i+1
        for i1 in range(size):
            if i1+i<=size:
                words.append(" ".join(s_ls[i1:i1+i]))
    return words
#读取黑名单关键
stopkeyword=r"C:\Users\ZG\Desktop\stopkeyword.csv"

#读取要清洗的数据
new_path=r"C:\Users\ZG\Desktop\mykeyword.csv"

#黑名单列表
stop_words=[]
with open(stopkeyword) as f:
    reader=csv.reader(f)
    for r in reader:
        word=r[4].strip()
        stop_words.append(word.lower())

print("获取完黑名单库",stop_words[0:15])

with open(new_path) as f_new:
    reader_new=csv.reader(f_new)
    n=0
    for new_r in reader_new:
        n=n+1
        #取出并处理每一个待检词
        word=new_r[0].strip()
        #判断一个关键词的所有相邻组合是否在黑名单中 如果在则不弄用这个关键词
        #计算所有组合
        words=find_words(word)
        for w in words:
            if w.lower() in stop_words:
                print("第{n}个词 {word}不能用,因为{w}".format(word=word,w=w,n=n))
