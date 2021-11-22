#conding="utf-8"
import time
from multiprocessing import Pool
import queue
import random
import os

def f(x):
    print("当前进程--",os.getpid())
    print('执行{x}'.format(x=x))
    n = random.randint(5, 10)
    time.sleep(n)
    print(x + x)
    print("\n\n")
    


if __name__ == '__main__':
    q = queue.Queue()
    for i in range(100000):
        q.put(i)
    #创建容量为100的进程池 
    pool=Pool(processes=100)
    while q.empty()!=True:
        #只要队列不空 一直提交进程执行
        pool.apply_async(f,args=(q.get(),))
    pool.close()
    pool.join()

    print("执行完毕")
