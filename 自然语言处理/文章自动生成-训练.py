from random import randint
from shutil import copyfile
import csv,time
def wordListSum(wordList):
    sum=0
    for word,value in wordList.items():
        sum+=value
    return sum
 
def retrieveRandomWord(wordList):
    randIndex=randint(0,wordListSum(wordList))
    for word,value in wordList.items():
        randIndex=randIndex-value
        if randIndex<=0:
            return word
 
def buildWordDict(text):
    #剔除换行符和引号
    text=text.replace("\n","")
    text=text.replace("\"","")
    text=text.replace("--","")
    #保证每个标点符号都和前面的单词在一起
    #这样不会被剔除，保留在马尔科夫链中
    punctuation=[',','.',';',':']
    for symbol in punctuation:
        text=text.replace(symbol," "+symbol+" ")
    words=text.split(" ")
    #过滤空单词
    words=[word for word in words if word !=""]
    
    wordDict={}
    for i in range(1,len(words)):
        if words[i-1] not in wordDict:
            #为单词新建一个字典
            wordDict[words[i-1]]={}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]]=wordDict[words[i-1]][words[i]]+1
    return wordDict
#更新字典
def merge(d1, d2):
    c = {}
    for k, v in d1.items():
        d3 = d1[k]
        if k in d2:
            #合并
            d4 = d2[k]
            if isinstance(d3, dict) and isinstance(d4, dict):
                c[k] = merge(d3, d4)
            else:
                c[k] = d1[k] + d2[k]
        else:
            c[k] = d1[k]

    for k, v in d2.items():
        d3 = d2[k]
        if not k in d1:
            c[k] = d3
    return c

#反转字符串
def s_ab(s):
    s1=s[::-1]
    return s1

def cp_new(f):
    import os.path
    if os.path.isfile(f):
        copyfile(f,f+r'.new')
        return f+r'.new'
    else:
        with open(f+r'.new','w'):
            return f+r'.new'

def wt_db(text,db_path):
    import os.path
    #生成结果字典
    newDict=buildWordDict(text)
    d=db_path
    #打开已有模型,如果模型不存在，则新建一个空字典
    if os.path.isfile(d):
        with open(d,'r',encoding='utf8') as f:
            s=f.read()
            try:
                oldDict=eval(s)
            except Exception as e:
                print(e)
                oldDict={}
    else:
        print('新建字典模型')
        oldDict={}
        
    #计算出新模型
    wordDict=merge(oldDict,newDict)

    #保存新模型
    #尝试保存
    test_path=cp_new(db_path)
    with open(test_path,'w',encoding='utf-8',errors='ignore') as f:
        f.write(str(wordDict))

    #正式保存
    d=db_path
    with open(d,'w',encoding='utf-8',errors='ignore') as f:
        f.write(str(wordDict))

#采集古腾堡
def find_txt(url):
    import requests,re
    req=requests.get(url)
    txt=req.text
    n1=txt.index("THE ENCOUNTER")
    n2=txt.index('*** START: FULL LICENSE ***')
    txt=txt[n1:n2]
    txt=re.sub(r'"|\/.\/','',txt)
    txt=re.sub('\r',' ',txt)
    return txt

dbA=r'D:\Backup\桌面\python文本处理\dbxs-a.txt'
dbB=r'D:\Backup\桌面\python文本处理\dbxs-b.txt'

while True:
    s=str(input('请输入:'))
    try:
        test_pathA=cp_new(dbA)
        wt_db(s,dbA)
        
        test_pathB=cp_new(dbB)
        wt_db(s_ab(s),dbB)
        print('完成')
    except Exception as e:
        print('跳出',e)
        continue
