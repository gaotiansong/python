#给它字符串 "gao tian song"
#输出 ["gao","tian","song","gao tian","tian song","gao tian song"]

def find_words(s):
    import re
    #计算一段文字所有相邻组合
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
