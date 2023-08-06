#-*- coding:utf8 -*-
### code by chengxz 2020/9/4 ####
import redis
from rediscluster import StrictRedisCluster


class TcRedis():
    def __init__(self,*nodelist):
        self.redisinst = None
        if len(nodelist) == 0:
            self.redisinst = redis.StrictRedis(host='localhost',port=6379,db=0)
        elif len(nodelist) == 1:
            host,port = nodelist[0].split(':')
            self.redisinst = redis.StrictRedis(host=host,port=int(port))
        elif len(nodelist) > 1:
            redis_nodes = []
            for node in nodelist:
                host,port = node.split(':')
                redis_nodes.append({"host":host,"port":int(port)})
            self.redisinst =StrictRedisCluster(startup_nodes=redis_nodes,decode_responses=True)

    def set(self,key,value):
        return self.redisinst.set(key,value)
    def get(self,key):
        return self.redisinst.get(key)
    def delete(self,key):
        return self.redisinst.delete(key)
    def ttl(self,key):
        return self.redisinst.ttl(key)
    def scan(self,cursor=0,match=None,count=2000):
        depth = 1000
        cursor = 0
        result = []
        for i in range(depth):
            cursor, result0 = self.redisinst.scan(cursor, match=match)
            if len(result0) != 0:
                result = result + result0
            if cursor == 0:
                break
        return result
    def hset(self,key,name,value):
        return self.redisinst.hset(key,name,value)
    def hget(self,key,name):
        return self.redisinst.hget(key, name)
    def lpush(self,key,*values):
        return self.redisinst.lpush(key,*values)
    def lpop(self,key):
        return self.redisinst.lpop(key)
    def sadd(self,key,*values):
        return self.redisinst.sadd(key,*values)
    def smembers(self,key):
        return self.redisinst.smembers(key)
    def zadd(self,key,*args,**kwargs):
        return self.redisinst.zadd(key,*args,**kwargs)
    def zrange(self,key,start,end):
        return self.redisinst.zrange(key,start,end)

if __name__ == "__main__":
    inst = TcRedis("172.17.9.60:16421")
    #print("set:",inst.set("a","aaaaaaaaaaaaaaaaaa"))
    #print("get:",inst.get("a"))
    #print(inst.scan(0,"*a*"))
    #print(inst.hset("hh","a","b"))
    #print(inst.hget("hh", "a"))
    #print(inst.lpush("list_test1","a","b"))
    #print(inst.lpop("list_test1"))
    #print(inst.sadd("set_test","a",'b'))
    #print(inst.smembers("set_test"))
    print(inst.zadd("zset_test",1.1,'name1','1.2','name2'))
    print(inst.zrange("zset_test",0,2))

