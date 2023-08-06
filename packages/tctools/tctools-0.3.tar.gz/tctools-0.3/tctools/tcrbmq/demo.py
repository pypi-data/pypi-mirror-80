#-*- coding:utf8 -*-

from tcrbmq import TcRbmq
import time,string,random
import logging

#logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S', filemode='a+')


rbinst = TcRbmq(['172.17.9.145','172.17.9.148'],close_queue='false')

def test_recv():
    global rbinst
    rbinst.bindqueue('test-bycxz1','rkey1','cxz-queue1','direct')
    res = rbinst.receive()
    #logging.info(res)
    print(res)

def test_send():
    global rbinst
    body = ''.join(random.sample(string.hexdigits * 10,20))
    print(body)
    rbinst.send(body,'test-bycxz1','rkey1','direct')

if __name__ == "__main__":
    for x in range(10):
        test_send()
    #test_send()
    print('->send finish.')
    time.sleep(3)
    test_recv()