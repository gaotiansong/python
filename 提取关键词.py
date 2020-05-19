import re
def getNgrams(content,n):
    content=content.split(' ')
    output=[]
    for i in range(len(content)-n+1):
        output.append(content[i:i+n])
    return output

def key_va(ngrams,content,n):
    a=[]
    b=[]
    for i1 in ngrams:
        if i1 in a:
            continue
        a.append(i1)
        if i1=='':
            continue
        n1=0
        for i2 in ngrams:
            if i1==i2:
                n1=n1+1
                keys=' '.join(i1)
        b.append({keys:n1})
    
    b.sort(key=lambda x: list(x.values()))
    d=list(b[-1].keys())[-1]
    v=list(b[-1].values())[-1]
    if v>2:
        n=n+1
        ngrams=getNgrams(content,n)
        s=key_va(ngrams,content,n)

    print(d)
    print(v)

filletxt=open(r'D:\Backup\桌面\python文本处理\test.txt','r',encoding='utf-8')
content=filletxt.read().lower()
content=re.sub(' |\n',' ',content)
content=re.sub(',',' ',content)
content=re.sub('./',' ',content)
n=1
ngrams=getNgrams(content,n)
filletxt.close()
key_va(ngrams,content,n)

