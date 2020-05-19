import re

def getNgrams(content,n):
    content=content.split(' ')
    output=[]
    for i in range(len(content)-n+1):
        output.append(content[i:i+n])
    return output


content=open(r'D:\Backup\桌面\python文本处理\test.txt','r',encoding='utf-8').read().lower()

content=re.sub(' |\n',' ',content)
content=re.sub(',',' ',content)
content=re.sub('./',' ',content)
a=[]
b=[]
ngrams=getNgrams(content,1)

for i1 in ngrams:
    if i1 in a:
        continue
    a.append(i1)

    if i1=='':
        continue
    n=0
    for i2 in ngrams:
        if i1==i2:
            n=n+1
    keys=' '.join(i1)
    b.append({keys:n})
    
        
b.sort(key=lambda x: list(x.values()))

print(b[:-1])
