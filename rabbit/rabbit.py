import sys
import json
import logging
import pika
from utils import AgentList

from config import SOCKET as sk

class RabbitQueue:
    def __init__(self, routing_key):
        self.logger = logging.getLogger("rabbit")
        self.routing_key = routing_key

    def connect(self):
        credentials = pika.PlainCredentials(sk["USER"], sk["PASSWD"])
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(sk["HOST"],sk["PORT"],'/',credentials))
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue= self.routing_key)

    def push(self, message):
        self.logger.debug("Function: RabbitQueue.push(%s), message: '%s'."%(self.routing_key, message))
        try:
            self.connect()
        except Exception as e:
            self.logger.error("Function: RabbitQueue.push '%s'."%(str(e)))
            try:
                self.connection.close()
            except Exception as e:
                pass
            return False
        self.channel.basic_publish(exchange='',
            routing_key = self.routing_key,
            properties=pika.BasicProperties(delivery_mode=2,),
            body = message)
        self.connection.close()
        return True

    def get(self, no_ack = True):
        self.logger.debug("Function: RabbitQueue.get(%s), from queue get all messages."%(self.routing_key))
        try:
            self.connect()
        except Exception as e:
            self.logger.error("Function: RabbitQueue '%s'."%(str(e)))
            try:
                self.connection.close()
            except Exception as e:
                pass
            return None
        self.channel = self.connection.channel()
        result = []
        for i in range(self.queue.method.message_count):
            body = self.channel.basic_get(queue=self.routing_key, no_ack=no_ack) # get queue basic with single queue
            result.append(body)
        self.connection.close()
        return result

class PushUnicast(object):
    """docstring for PushUnicast"""
    def __init__(self):
        self.logger = logging.getLogger("rabbit")
        self.al = AgentList()

    def push_to_origin_group(self, message):
        origin_list = self.al.get_origin()
        self.logger.debug(origin_list)
        if not origin_list["status"] == 200:
            self.logger.error(origin_list["message"])
            return 1
        for i in origin_list["data"]:
            rb = RabbitQueue(i["ip"])
            rb.push(message)
        return 0

    def push_to_4500_group(self, message):
        agent_4500_list = self.al.get_4500()
        self.logger.debug(agent_4500_list)
        if not agent_4500_list["status"] == 200:
            self.logger.error(agent_4500_list["message"])
            return 1
        for i in agent_4500_list["data"]:
            rb = RabbitQueue(i["ip"])
            rb.push(message)
        return 0

    def push_to_ott_group(self, message):
        ott_list = self.al.get_ott()
        self.logger.debug(ott_list)
        if not ott_list["status"] == 200:
            self.logger.error(ott_list["message"])
            return 1
        for i in ott_list["data"]:
            rb = RabbitQueue(i["ip"])
            rb.push(message)
        return 0
        
