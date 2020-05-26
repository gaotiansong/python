from random import choice, randint
from urllib.request import urlopen
import time

def wordListSum(wordList):
    sum=0
    for word,value in wordList.items():
        sum+=value
        word=word
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

#判断最后一个‘.’位置
def indexstr(str1,str2):
    '''查找指定字符串str1包含指定子字符串str2的全部位置，
    以列表形式返回'''
    lenth2=len(str2)
    lenth1=len(str1)
    indexstr2=[]
    i=0
    while str2 in str1[i:]:
        indextmp = str1.index(str2, i, lenth1)
        indexstr2.append(indextmp)
        i = (indextmp + lenth2)
    return indexstr2[-1]

#生成链长为100的马尔科夫链
def pr_text():
    with open(r'D:\Backup\桌面\python文本处理\db.txt') as f:
        r=f.read()
        wordDict=eval(r)

    length=200
    #抽取一个词作为开始，这个词第一个字母必须为大写
    while True:
        s=choice(list(wordDict))
        if s.istitle():
            break

    chain=[s]
    #currentWord=" "
    for i in range(0,length):
        try:
            keylist=wordDict[chain[-1]]
        except Exception as e:
            continue
        newWord=retrieveRandomWord(keylist)
        chain.append(newWord)
    s=' '.join(chain)
    try:
        n=indexstr(s,'.')
        s=s[:n+1]
    except Exception as e:
        print(e)
    return s

while True:
    s=pr_text()
    if len(s)<150:
        continue
    print(s+'\n')
    time.sleep(10)
