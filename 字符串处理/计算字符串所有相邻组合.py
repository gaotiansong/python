#给它字符串 "zhe xue jia"
#输出 ["zhe","xue","jia","zhe xue","xue jia","zhe xue jia"]

def find_words(s):
    import re
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
