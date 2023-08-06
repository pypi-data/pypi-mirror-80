#-*- coding:utf8 -*-

from tcrkmq import TcRkmq
import random,string,time

rkinst = TcRkmq()

def test_send():
    global rkinst
    body = ''.join(random.sample(string.hexdigits * 10, 20))
    #body = '中国'
    print(body)
    rkinst.send('jmqs_test_rid_product',body)
    rkinst.send('jmqs_test_rid_product', body.encode())

def test_receive():
    global rkinst
    res = rkinst.receive('jmqs_test_rid_consume')
    print(res)
    print('size',len(res))

if __name__ == "__main__":
    for x in range(10):
        test_send()
    print('->send finish')
    #test_send()
    time.sleep(3)
    test_receive()