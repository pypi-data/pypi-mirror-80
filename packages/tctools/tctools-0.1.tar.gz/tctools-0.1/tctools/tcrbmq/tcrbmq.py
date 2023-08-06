#-*- coding:utf -*-

import pika

class TcRbmq():
    def __init__(self,hosts=[],user='push',passwd='testmq',**kwargs):
        self.mq_ip_channel_conn = {}
        self.hosts = hosts
        self.user = user
        self.passwd = passwd

        self.close_queue = True
        if 'close_queue' in kwargs:
            if kwargs['close_queue'] == 'false':
                self.close_queue = False
        ##
        self.ex_name = None
        self.ex_type = None
        self.rkey_name = None
        self.queue_name = None
        self.ex_durable = False
        self.queue_durable = False

    def getConn(self,ip):

        if ip in self.mq_ip_channel_conn.keys():
            channel = self.mq_ip_channel_conn[ip]['channel']
            connection = self.mq_ip_channel_conn[ip]['connection']
            return channel, connection

        credentials = pika.PlainCredentials(self.user, self.passwd)
        parameters = pika.ConnectionParameters(ip, 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        mq_ip_tmp = {}
        mq_ip_tmp['channel'] = channel
        mq_ip_tmp['connection'] = connection
        self.mq_ip_channel_conn[ip] = mq_ip_tmp

        return channel, connection

    def _bindqueue(self,channel, **kw):
        channel.exchange_declare(exchange=self.ex_name, exchange_type=self.ex_type,durable=self.ex_durable)

        channel.queue_declare(queue=self.queue_name,durable=self.queue_durable)

        channel.queue_bind(exchange=self.ex_name, queue=self.queue_name, routing_key=self.rkey_name)

    def bindqueue(self,ex_name, rkey_name, queue_name, ex_type, **kwargs):

        ##init
        self.ex_name = ex_name
        self.rkey_name = rkey_name
        self.queue_name = queue_name
        self.ex_type = ex_type
        if 'ex_durable' in kwargs:
            if kwargs['ex_durable'] == 'true':
                self.ex_durable = True
        if 'queue_durable' in kwargs:
            if kwargs['queue_durable'] == 'true':
                self.queue_durable = True
        if 'clear' in kwargs:
            pass

        for ip in self.hosts:
            # 1.清理队列历史数据
            # 2.得到MQ连接
            channel, connection = self.getConn(ip)
            # 3.队列绑定
            self._bindqueue(channel)
            # 4.生产数据
            # send(ip,'hellomessage_%s_2'%(ip),ex_name,ex_type,rkey_name,queue_name,ex_durable='true',queue_durable='true')
            # 5.关闭连接
            # closeConnect(channel,connection)

    def send(self,msg, ex, rkey,ex_type, ex_durable='false'):
        ex_durable_b = False
        queue_durable_b = False
        if ex_durable == 'true':
            ex_durable_b = True
        for ip in self.hosts:
            channel, connection = self.getConn(ip)
            channel.exchange_declare(exchange=ex, exchange_type=ex_type, durable=ex_durable_b)
            #channel.queue_declare(queue=queue_name, durable=queue_durable_b)
            #channel.queue_bind(exchange=ex, queue=queue_name, routing_key=rkey)
            channel.basic_publish(exchange=ex, routing_key=rkey, body=msg)

    def _receive(self,channel):

        method_frame, header_frame, body = channel.basic_get(queue='%s' % (self.queue_name))
        if method_frame is None:
            return None
        if method_frame.NAME == 'Basic.GetEmpty':
            return None
        else:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            return body

    def receive(self, **kw):
        res = []

        for h in self.hosts:
            # 1.获取MQ连接
            channel, connection = self.getConn(h)
            # 2.消费数据
            body = self._receive(channel)
            while body is not None:
                # print(body)
                res.append(body)
                body = self._receive(channel)
        return res

    def unbindqueue(self,channel):
        if self.ex_name is not None and self.close_queue:
            channel.queue_unbind(exchange=self.ex_name, queue=self.queue_name, routing_key=self.rkey_name)

    def closeConnect(self,channel, connection):
        channel.close()
        connection.close()

    def close_mq_queue(self,**kw):

        for ip in self.hosts:
            if ip in self.mq_ip_channel_conn.keys():
                channel = self.mq_ip_channel_conn[ip]['channel']
                connection = self.mq_ip_channel_conn[ip]['connection']
                self.unbindqueue(channel)
                self.closeConnect(channel, connection)

    def __del__(self):
        self.close_mq_queue()