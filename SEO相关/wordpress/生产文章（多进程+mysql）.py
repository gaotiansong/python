from random import choice, randint
from urllib.request import urlopen
from multiprocessing import Process,Queue
import time,random,os
import pymysql,csv,re

#获取关键词列表
def find_keys(key,n):
    conn = pymysql.connect(
        host="192.168.1.37",
        port=3307,
        user="root",password="123456",
        database="keyword",
        charset="utf8")

    cur=conn.cursor()
    #sql="SELECT * FROM shose ORDER BY RAND() LIMIT 1;"
    sql="SELECT word,vo FROM key_full WHERE word like '%{key}%' and vo>'{n}' ;".format(key=key,n=n)
    cur.execute(sql)
    row=cur.fetchall()
    s=[]
    for i in row:
        s.append(i)
    keyword=choice(s)
    conn.commit()
    cur.close()
    conn.close()
    return keyword[0],keyword[1]

#获取一个关键词
def find_key(word,vo):
    key=find_keys(word,vo)[0]
    return key

#获得单篇内容,   
def find_des(dbA,dbB):
    n=1
    while True:
        keyword=find_key('shoes',200)
        keyword=re.sub('\.|\?|:','',keyword)
        try:
            d=write_page(dbA,dbB,keyword)
        except Exception as e:
            print(e)
            continue
        name=d['h1']
        if len(name)<60:
            name=name+' '+find_key('shoes',0)
        des=d['content']
        post_tag=[find_key('shoes',0),find_key('nike',0),find_key('shoes',0)]
        category=[find_key('shoes',200)]
        des=(name,des,post_tag,category)
        return des

def retrieveRandomWord(wordList):
    randIndex=randint(0,wordListSum(wordList))
    for word,value in wordList.items():
        randIndex=randIndex-value
        if randIndex<=0:
            return word

def wordListSum(wordList):
    sum=0
    for word,value in wordList.items():
        sum+=value
        word=word
    return sum

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

#把文本变成字典
def find_dict(db_path):
    with open(db_path,encoding='utf8') as f:
        r=f.read()
        wordDict=eval(r)
    return wordDict

#生成链长为100的马尔科夫链
def pr_text(keyword,wordDict):
    length=300
    #设置装关键词的列表
    chain=[keyword]
    #循环length次,每次取一个关键词放入列表，最后组合成句子

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
    n=indexstr(s,'.')
    s=s[:n+1]
    return s

def pr_text_b(keyword,wordDict):
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
    s1=pr_text_b(s_ab(ka),dicB)
    s1=s_ab(s1)
    #得出后半截文本
    s2=pr_text(kb,dicA)
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

    #如果文本长度小于某个随机数，即设置一篇文章的长度范围
    while len(txt)<randint(100,1000):
        txt=writing(keyword)

    while len(txt)<1000:
        txt=txt+'<br><br>'+writing(keyword)

    d={'title':keyword,
        'h1':keyword,
        'content':txt,
        'context':'这是next',
        'relevant':'这是相关'
        }
    return d

#把文章写入网站
def wt_wordpress(in_q,wp_user):
    name,des,post_tag,category=in_q
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
    xmrpc_url,user,password=wp_user
    wp = Client(xmrpc_url,user,password) 
    
    post.terms_names = { 
        'post_tag':post_tag, #文章所属标签，没有则自动创建
        'category':category #文章所属分类，没有则自动创建
        }

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

#多进程相关

#生成器，用来无限生成数字
def find_n():
    a=0
    while True:
        yield a
        a=a+1
#消费
def consumer(q,n):
    for i in find_n():
        if q.empty():
            print('库存没了，等待生产')
            time.sleep(5)
            pass
        else:
            s=q.get()
            print('{}进程写入网站{}次'.format(n,i))
            wt_wordpress(s,wp_user)
            time.sleep(random.randint(2,5))
#生产
def producer(q,n):
    print('生产线程')
    for i in find_n():
        print('库存',q.qsize())
        if q.full():
            time.sleep(5)
        else:
            s=find_des(dbA,dbB)
            q.put(s)
            time.sleep(random.randint(0,3))


dbA=r'F:\py\mysql\鞋子模型\shose-a.txt'
dbB=r'F:\py\mysql\鞋子模型\shose-b.txt'
wp_user=('http://abc.com/xmlrpc.php', 'admin', '123147gts')

dicA=find_dict(dbA)
dicB=find_dict(dbB)

if __name__ == '__main__':
    #设置队列容量，队列容量过大可能导致更多消耗内存
    q=Queue(50)
    print('开始干！干！干！干！')
    #设置生产文章的线程数
    for i in range(30):
        i=Process(target=producer,args=(q,i)).start()
        time.sleep(3)


    #写入文章，设置写入文章的线程数
    for i in range(5):
        i=Process(target=consumer,args=(q,i)).start()
