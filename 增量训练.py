from random import randint

d1={'a':{'a1':1,'a2':2},'b':{'b1':1,'b2':1},'c':{'c1':1,'c2':1}}

d2={'a':{'a1':100,'a2':2,'a3':4},'d':{'d1':1,'d2':2},'c':{'c2':1,'c3':2}}

#如果d1中木有这个建，则把d2中的建和值加入到d1中
for i in d2:
    if i not in d1:
        d1[i]=d2[i]
#print(d1)
#如果d1中有这个键,则把这两个键的值相加后赋给这个键

for i1 in d1:
    for i2 in d2:
        #如果这两个字典的键相同,则对比子字典中的项目
        if i1==i2:
            #如果两个子字典的值不同，则有两种情况，子字典1中木有的键直接添加，存在的键值相加，键不变
            if d1[i1]!=d2[i2]:
                for k22,v22 in d2[i2].items():
                    for k11,v11 in d1[i1].items():
                        x={}
                        #如果两个子字典的键相同，则值相加
                        if k11==k22:
                            d1[i1][k11]=v11+v22
                        else:
                            x[k22]=v22
                    d1[i1].update(x)
print(d1)
