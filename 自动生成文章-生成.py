from random import choice, randint
from urllib.request import urlopen
import time,re
import csv

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
def pr_text(keyword,db_path):
    #打开文本，把内容转换为字典
    with open(db_path,encoding='utf8') as f:
        r=f.read()
        wordDict=eval(r)
    
    length=300
    #设置装关键词的列表
    chain=[keyword]
    #循环length次,每次取一个关键词放入列表，最后组合成句子
    '''
    for i in range(0,length):
        print(i)
        try:
            keylist=wordDict[chain[-1]]
        except Exception as e:
            continue
        newWord=retrieveRandomWord(keylist)
        chain.append(newWord)
    '''
    n=0
    while n<length:
        try:
            keylist=wordDict[chain[-1]]
        except Exception as e:
            print(e)
            break
        newWord=retrieveRandomWord(keylist)
        chain.append(newWord)
        n=n+1
    chain=chain[1:]
    s=' '.join(chain)

    #最后一个'.'的位置为一段话的结束，保证句子的完整性。
    '''
    try:
        n=indexstr(s,'.')
        #句子要包括最后的'.'
        s=s[:n+1]
    except Exception as e:
        print('获取文本S',e,s)
    '''
    n=indexstr(s,'.')
    s=s[:n+1]
    return s

def pr_text_b(keyword,db_path):
    with open(db_path,encoding='utf8') as f:
        r=f.read()
        wordDict=eval(r)
    length=randint(1000,5000)
    chain=[keyword]
    for i in range(0,length):
        try:
            keylist=wordDict[chain[-1]]
        except Exception as e:
            continue
        newWord=retrieveRandomWord(keylist)
        if newWord in '!,.?/n:;?':
            break
        chain.append(newWord)
    chain=chain[1:]
    s=' '.join(chain)
    return s

#反转字符串
def s_ab(s):
    s1=s[::-1]
    return s1

#获取关键词的头尾词
def h_t(s):
    s1=s.split(' ')
    s_a=s1[0]
    s_b=s1[-1]
    return s_a,s_b

#得出拼接好的文本
def writing(keyword):
    ka,kb=h_t(keyword)
    #得出前半截文本
    s1=pr_text_b(s_ab(ka),dbB)
    s1=s_ab(s1)
    #得出后半截文本
    s2=pr_text(kb,dbA)
    #拼接成完整文本
    txt=s1+' '+keyword+' '+s2
    return txt


def to_html(d,tem):
    with open(tem,"r") as f:
        t=f.read()
        html=t.format_map(d)
        return html

def write_in(s,path):
    with open(path,'w') as f:
        f.write(s)

def write_page(dbA,dbB,keyword):
    txt=writing(keyword)
    
    #如果文本小于某个随机数
    while len(txt)<randint(100,1000):
        txt=writing(keyword)

    while len(txt)<1000:
        #print(len(txt))
        txt=txt+'<br><br>'+writing(keyword)
        #print(len(txt))

    d={'title':keyword,
        'h1':keyword,
        'content':txt,
        'context':'这是next',
        'relevant':'这是相关'
        }
    return d

#把内容写入wordpress
def wt_wordpress(name,des):
    from wordpress_xmlrpc import Client, WordPressPost
    from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
    from wordpress_xmlrpc.methods.users import GetUserInfo
    from wordpress_xmlrpc.methods import posts
    from wordpress_xmlrpc.methods import taxonomies
    from wordpress_xmlrpc import WordPressTerm
    from wordpress_xmlrpc.compat import xmlrpc_client
    from wordpress_xmlrpc.methods import media, posts
    import sys
    import importlib
    import random
     
    importlib.reload(sys)
     
    post = WordPressPost()
    post.title = name
    post.content = des
    post.post_status = 'publish' #文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
    wp = Client('https://customp.cn/xmlrpc.php', 'customp', 'PYOqDvyjw2F6vQGir%pnd1PQ') 
    '''
    post.terms_names = { 
        'post_tag':seokey(key_tag,30,3), #文章所属标签，没有则自动创建
        'category':seokey(key_category,20000,2) #文章所属分类，没有则自动创建
        }
    '''
 
    post.custom_fields = []   #自定义字段列表
    post.custom_fields.append({  #添加一个自定义字段
        'key': 'price',
        'value': 3
        })
 
    post.custom_fields.append({ #添加第二个自定义字段
        'key': 'ok',
        'value': 'customfw.com'
        })
    post.id = wp.call(posts.NewPost(post))
    time.sleep(1)

#设置文本模型库
dbA=r'D:\Backup\桌面\python文本处理\am\db-a.txt'
dbB=r'D:\Backup\桌面\python文本处理\am\db-b.txt'
#设置html模板
tem=r"D:\Backup\桌面\\python文本处理\a\a.txt"
#设置内容生成路径
html_path=r"D:\Backup\桌面\\python文本处理\\a\\"

#设置关键词列表
keywords=r'C:\Users\MyPC\Downloads\pillow-phrase_related-us.csv'

with open(keywords,encoding='utf8') as f:
    ks=csv.reader(f)
    n=1
    k_old=''
    for k in ks:
        if k[0] not in '关键词' and len(k[0])<=30:
            keyword=k[0]
            keyword=re.sub('\?|\!|\.','',keyword)
            #print(keyword)
            #生成内容主体
            try:
                d=write_page(dbA,dbB,keyword)
            except Exception as e:
                print(e,'生成内容失败')
                continue
            name=d['h1']
            des=d['content']
            try:
                wt_wordpress(name,des)
            except Exception as e:
                print(e,'写入失败')
            print(n,'篇')
            n=n+1
