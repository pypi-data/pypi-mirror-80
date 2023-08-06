#-*- coding:utf8 -*-
### code by chengxz 2020/9/4 ####

from tcredis import TcRedis

def test1():
    inst = TcRedis('172.17.9.60:16421')
    assert True == inst.set("test1_key", "bbb")
    assert b'bbb' == inst.get("test1_key")
    assert -1 == inst.ttl('test1_key')
    assert 1 == inst.hset("hash_test","a1","b")
    assert b'b' == inst.hget('hash_test','a1')
    assert 2 == inst.lpush("list_test1","a","b")
    assert b'b' == inst.lpop("list_test1")
    assert 2 == inst.sadd("set_test","a",'b')
    assert 2 == len(inst.smembers("set_test"))
    assert 2 == inst.zadd("zset_test",1.1,'name1','1.2','name2')
    assert b'name1' in inst.zrange("zset_test",0,2)
    assert 1 == inst.delete('test1_key')
    assert 1 == inst.delete('hash_test')
    assert 1 == inst.delete('list_test1')
    assert 1 == inst.delete('set_test')
    assert 1 == inst.delete('zset_test')

def test2():
    inst = TcRedis('172.17.9.71:9000','172.17.9.71:9001','172.17.9.71:9002')
    assert True == inst.set("test2_key", "bbb")
    assert 'bbb' == inst.get("test2_key")
    assert -1 == inst.ttl('test1_key')
    assert 1 == inst.hset("hash_test","a1","b")
    assert 'b' == inst.hget('hash_test','a1')
    assert 2 == inst.lpush("list_test1","a","b")
    assert 'b' == inst.lpop("list_test1")
    assert 2 == inst.sadd("set_test","a",'b')
    assert 2 == len(inst.smembers("set_test"))
    assert 2 == inst.zadd("zset_test",1.1,'name1','1.2','name2')
    assert 'name2' in inst.zrange("zset_test",0,2)
    assert 1 == inst.delete('test2_key')
    assert 1 == inst.delete('hash_test')
    assert 1 == inst.delete('list_test1')
    assert 1 == inst.delete('set_test')
    assert 1 == inst.delete('zset_test')

if __name__ == "__main__":
    test1()
    test2()