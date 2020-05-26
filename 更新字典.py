# coding=utf-8

d1={'a':{'a1':1,'a2':2},'b':{'b1':1,'b2':1},'c':{'c1':1,'c2':1},'e':{'e1':1},'f':{'f1':2,'f2':5,'f3':7},'g':{'g1':2}}

d2={'a':{'a1':100,'a2':2,'a3':4},'d':{'d1':1,'d2':2},'c':{'c2':1,'c3':2},'e':{'e1':1},'f':{'f1':2,'f2':1},'g':{'g1':2}}

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

m = merge(d1, d2)
print ('m = ', m)
