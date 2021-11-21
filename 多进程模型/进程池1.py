from multiprocessing import Pool
import time
import os
import random
def action(name):
    n=random.randint(1,5)
    print(name,' --当前进程：',os.getpid(),"等待",n)
    time.sleep(n)
    print("结束",n)
if __name__ == '__main__':
    #创建包含 4 条进程的进程池
    pool = Pool(processes=5)
    # 将action分3次提交给进程池
    for i in range(30):
        pool.apply_async(action, args=(i, ))
    pool.close()
    pool.join()
