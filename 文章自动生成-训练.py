from random import randint
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

def wt_db(text):
    #训练素材 
    #text=open(r'D:\Backup\桌面\python文本处理\inaugurationSpeech.txt',encoding='utf-8').read()

    #生成结果字典
    newDict=buildWordDict(text)

    #打开已有模型,如果模型不存在，则新建一个空字典
    try:
        d=r'D:\Backup\桌面\python文本处理\db.txt'
        with open(d,'r') as f:
            s=f.read()
            oldDict=eval(s)
    except Exception as e:
        print(e)
        oldDict={}

    #计算出新模型
    wordDict=merge(oldDict,newDict)


    #保存新模型
    d=r'D:\Backup\桌面\python文本处理\db.txt'
    with open(d,'w',encoding='utf-8',errors='ignore') as f:
        f.write(str(wordDict))


with open(r'D:\Backup\桌面\python文本处理\帽子语料\Baseball cap.csv','r',encoding='utf-8',errors='ignore') as f:
    readCsv=csv.reader(f)
    n=0
    for i in readCsv:
        n+=1
        if i[0]=='Name':
            continue
        s=i[0]+' '+i[2]
        wt_db(s)
        print(n,'条')
