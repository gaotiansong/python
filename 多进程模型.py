from multiprocessing import Process,Queue
import time,random,os
def consumer(q):
    for i in find_n():
        if q.empty():
            print('仓库空了，暂停消费')
            time.sleep(1)
            pass
        else:
            print('消费',i)
            q.get()
            time.sleep(random.randint(2,5))
#生产
def producer(q):
    for i in find_n():
        if q.full():
            print('仓库满了，暂停生产！')
            time.sleep(1)
        else:
            print('生产',i)
            q.put('产品')
            time.sleep(random.randint(0,3))

def find_n():
    a=0
    while True:
        yield a
        a=a+1

q=Queue(10)
#生产者们:即厨师们

p1=Process(target=producer,args=(q,))

#消费者们:即吃货们
c1=Process(target=consumer,args=(q,))

#开始
p1.start()
c1.start()
print('主')
